import { mkdtempSync, rmSync } from "node:fs";
import http from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { runInNewContext } from "node:vm";
import { canonicalJson } from "../encoding.js";
import { TaskExecutor, UnreportedError } from "../executor.js";
import { flow } from "../flow.js";
import { TaskRegistry } from "../registry.js";
import { task } from "../task.js";
import type {
  CallbackRequest,
  RegisterTaskOptions,
  StepAttemptRecord,
  StepAttemptRequest,
  StepCompleteRequest,
  StepRecord,
  StepStartRequest,
  WaitResponse,
} from "../types.js";
import { UDSClient } from "../uds.js";
import { FlowFailedError, StepError } from "./errors.js";

const b64 = (value: unknown) => Buffer.from(JSON.stringify(value)).toString("base64");
const unb64 = (value: string) => JSON.parse(Buffer.from(value, "base64").toString());

const RETRY_NOT_ALLOWED_RE = /retry policy is not allowed on a workflow/;
const ONE_STEP_RE = /one step at a time/;
const WITHIN_STEP_RE = /ctx\.step can't be called within a step: step "nested"/;
const NAME_FIRST_RE = /takes the step's name first/;
const EMPTY_NAME_RE = /needs a non-empty step name/;
const NESTED_WORKFLOW_RE = /can't run another workflow/;
const USE_STEP_RE = /use ctx\.step to run a function/;
const USE_INVOKE_RE = /is a registered task; use ctx\.invoke to run it/;
const INVOKE_UNSUPPORTED_RE = /ctx\.invoke\(invoice\): .* isn't supported yet/;
const SLEEP_UNSUPPORTED_RE = /ctx\.sleep: .* isn't supported yet/;
const HTTP_422_RE = /HTTP 422/;
const CIRCULAR_ENCODING_RE = /circular|cyclic/i;

type InlineKind = "start" | "attempt" | "complete";

interface InlineRequests {
  start: StepStartRequest;
  attempt: StepAttemptRequest;
  complete: StepCompleteRequest;
}

interface Injected {
  status: number;
  body: unknown;
  remaining?: number;
}

/**
 * A stand-in for renderd and the Step History Service, speaking the socket
 * protocol over a real Unix socket. Step writes are first-writer-wins, and
 * each execution sees the history recorded so far, so running the executor
 * again is a replay.
 */
class FakeDurableServer {
  attempt = 0;
  readonly steps = new Map<number, StepRecord>();
  readonly stepAttempts: StepAttemptRecord[] = [];
  readonly callbacks: CallbackRequest[] = [];
  readonly requests: { path: string; body: any }[] = [];
  wait: (childRunId: string) => WaitResponse = () => ({
    action: "done",
    complete: { output: b64(["child result"]) },
  });
  /** Answer the next request(s) to a path with this status instead. */
  readonly inject = new Map<string, Injected>();
  /** Runs before a /step-inline/<kind> request is applied. */
  beforeInline?: (kind: InlineKind, body: any) => void;

  readonly socketPath: string;
  private readonly dir: string;
  private readonly server: http.Server;

  constructor(
    private readonly taskName: string,
    private readonly args: unknown[] = [],
  ) {
    this.dir = mkdtempSync(join(tmpdir(), "rnd-"));
    this.socketPath = join(this.dir, "s.sock");
    this.server = http.createServer((req, res) => this.handle(req, res));
  }

  start(): Promise<void> {
    return new Promise((resolve) => this.server.listen(this.socketPath, resolve));
  }

  async stop(): Promise<void> {
    await new Promise((resolve) => this.server.close(resolve));
    rmSync(this.dir, { recursive: true, force: true });
  }

  /** Run one workflow attempt. Each call after the first is a replay. */
  async execute(): Promise<{ outcome?: string; error?: unknown }> {
    try {
      const outcome = await new TaskExecutor(this.socketPath).executeTask();
      return { outcome };
    } catch (error) {
      return { error };
    } finally {
      this.attempt++;
    }
  }

  paths(): string[] {
    return this.requests.map((r) => r.path);
  }

  inline<K extends InlineKind>(kind: K): InlineRequests[K][] {
    return this.requests.filter((r) => r.path === `/step-inline/${kind}`).map((r) => r.body);
  }

  lastCallback(): CallbackRequest {
    const callback = this.callbacks.at(-1);
    if (!callback) {
      throw new Error("no callback");
    }
    return callback;
  }

  output(): unknown {
    const output = this.lastCallback().complete?.output;
    if (output === undefined) {
      throw new Error(`no completed callback: ${JSON.stringify(this.lastCallback())}`);
    }
    return output === "" ? undefined : unb64(output)[0];
  }

  private handle(req: http.IncomingMessage, res: http.ServerResponse): void {
    const chunks: Buffer[] = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      // Route on the path alone; GET /input carries startup timestamps as a query.
      const path = (req.url ?? "").split("?")[0];
      const raw = Buffer.concat(chunks).toString();
      const body = raw ? JSON.parse(raw) : undefined;
      this.requests.push({ path, body });

      const injected = this.inject.get(path);
      if (injected) {
        injected.remaining = (injected.remaining ?? 1) - 1;
        if (injected.remaining === 0) this.inject.delete(path);
        res.statusCode = injected.status;
        res.end(JSON.stringify(injected.body));
        return;
      }

      res.setHeader("Content-Type", "application/json");
      res.end(JSON.stringify(this.respond(path, body) ?? null));
    });
  }

  private respond(path: string, body: any): unknown {
    const now = new Date().toISOString();
    switch (path) {
      case "/input":
        return {
          task_name: this.taskName,
          input: b64(this.args),
          task_run_id: "trn-wf",
          is_workflow: true,
          attempt: this.attempt,
          history:
            this.attempt === 0
              ? {}
              : {
                  steps: [...this.steps.values()].sort((a, b) => a.step_key.seq - b.step_key.seq),
                  step_attempts: this.stepAttempts,
                },
        };
      case "/callback":
        this.callbacks.push(body);
        return undefined;
      case "/step-inline/start":
        this.beforeInline?.("start", body);
        return this.stepStart(body, now);
      case "/step-inline/attempt":
        this.beforeInline?.("attempt", body);
        return this.stepAttempt(body, now);
      case "/step-inline/complete":
        this.beforeInline?.("complete", body);
        return this.stepComplete(body);
      case "/run-subtask": {
        const childRunId = `child-${body.step_key.seq}`;
        this.record({
          ...this.base(body, now),
          type: "invoked",
          task_name: body.task_name,
          input: body.input,
          child_run_id: childRunId,
        });
        return { task_run_id: childRunId };
      }
      case "/step-wait": {
        const answer = this.wait(body.child_run_id);
        const row = this.steps.get(body.seq);
        if (answer.action === "done" && row && !row.completed_at) {
          row.completed_at = now;
          row.workflow_attempt = this.attempt;
          if (answer.complete) row.output = answer.complete.output;
          if (answer.error) row.error = { name: "TaskError", message: answer.error.details };
        }
        return answer;
      }
      default:
        return undefined;
    }
  }

  private base(body: any, now: string) {
    return {
      step_key: body.step_key,
      // Set by the completion, not the start.
      workflow_attempt: 0,
      started_at: now,
    };
  }

  private record(row: StepRecord): void {
    if (!this.steps.has(row.step_key.seq)) {
      this.steps.set(row.step_key.seq, row);
    }
  }

  private stepStart(body: StepStartRequest, now: string): unknown {
    const row = this.steps.get(body.step_key.seq);
    if (row) {
      return { applied: false, step: row };
    }
    this.record({
      ...this.base(body, now),
      type: "inline",
      task_name: body.task_name,
      input: body.input,
    });
    return { applied: true };
  }

  private stepAttempt(body: StepAttemptRequest, now: string): unknown {
    const exists = this.stepAttempts.some(
      (a) => a.step_key.seq === body.step_key.seq && a.attempt === body.attempt,
    );
    if (!exists) {
      this.stepAttempts.push({
        step_key: body.step_key,
        attempt: body.attempt,
        workflow_attempt: this.attempt,
        error: body.error,
        started_at: body.started_at,
        ended_at: now,
      });
    }
    return { applied: !exists };
  }

  /** Mirrors renderd's checks on a completion, then records it first-writer-wins. */
  private stepComplete(body: StepCompleteRequest): unknown {
    const { key, outcome } = body;
    const final = outcome.final_attempt;
    if (body.session_id !== "trn-wf" || !outcome.completed_at) {
      throw new Error(
        `complete needs the run's session_id and completed_at: ${JSON.stringify(body)}`,
      );
    }
    if (outcome.output && final) {
      throw new Error("complete has both an output and a final attempt");
    }
    if (
      final &&
      (final.session_id !== body.session_id ||
        final.key.seq !== key.seq ||
        final.ended_at !== outcome.completed_at)
    ) {
      throw new Error(`final attempt doesn't match its completion: ${JSON.stringify(body)}`);
    }
    const row = this.steps.get(key.seq);
    if (!row) {
      throw new Error(`complete with no start row for seq ${key.seq}`);
    }
    if (row.completed_at) {
      return { applied: false, outcome: { output: row.output, error: row.error } };
    }
    if (final) {
      const error = unb64(final.error.data ?? "");
      const attempt: StepAttemptRecord = {
        step_key: key,
        attempt: final.attempt,
        // Like renderd: every write carries the session's workflow attempt.
        workflow_attempt: this.attempt,
        error,
        started_at: final.started_at,
        ended_at: final.ended_at,
      };
      // Like the Step History Service: a final attempt may reuse a recorded
      // attempt number only if it is the same attempt.
      const recorded = this.stepAttempts.find(
        (a) => a.step_key.seq === key.seq && a.attempt === final.attempt,
      );
      if (recorded && canonicalJson(recorded) !== canonicalJson({ ...recorded, ...attempt })) {
        throw new Error(`final attempt ${final.attempt} differs from the recorded one`);
      }
      if (!recorded) this.stepAttempts.push(attempt);
      row.error = error;
    }
    row.workflow_attempt = this.attempt;
    row.completed_at = outcome.completed_at;
    if (outcome.output?.data !== undefined) row.output = outcome.output.data;
    return { applied: true };
  }
}

describe("workflow", () => {
  let server: FakeDurableServer;

  beforeEach(() => {
    TaskRegistry.getInstance().clear();
  });

  afterEach(async () => {
    vi.restoreAllMocks();
    await server?.stop();
  });

  async function serve(name: string, args: unknown[] = []): Promise<FakeDurableServer> {
    server = new FakeDurableServer(name, args);
    await server.start();
    return server;
  }

  describe("registration", () => {
    it("rejects a retry policy from an untyped caller", () => {
      const options: any = { name: "wf", retry: { maxRetries: 1, waitDurationMs: 0 } };
      expect(() => flow(options, () => 1)).toThrow(RETRY_NOT_ALLOWED_RE);
      expect(TaskRegistry.getInstance().has("wf")).toBe(false);
    });

    it("marks workflows when registering", async () => {
      task({ name: "plain" }, () => 1);
      flow({ name: "wf", plan: "starter" }, () => 1);
      await serve("unused");

      await new TaskExecutor(server.socketPath).registerTasks();

      expect(server.requests).toEqual([
        {
          path: "/register-tasks",
          body: {
            tasks: [
              { name: "plain" },
              { name: "wf", options: { plan: "starter" }, workflow: true },
            ],
          },
        },
      ]);
    });

    it("lets a later registration replace one of the other kind", () => {
      const registry = TaskRegistry.getInstance();
      task({ name: "shared" }, () => 1);
      flow({ name: "shared" }, () => 1);
      expect(registry.has("shared")).toBe(false);
      expect(registry.getFlow("shared")?.name).toBe("shared");

      task({ name: "shared" }, () => 1);
      expect(registry.has("shared")).toBe(true);
      expect(registry.getFlow("shared")).toBeUndefined();
    });
  });

  describe("inline steps", () => {
    it("records each step and memoizes it on replay", async () => {
      let calls = 0;
      function double(n: number) {
        calls++;
        return n * 2;
      }
      flow({ name: "wf" }, async (ctx, n: number) => {
        const a = await ctx.step("double", double, [n]);
        const b = await ctx.step("plusOne", () => a + 1);
        return [a, b, ctx.metadata];
      });
      await serve("wf", [5]);

      expect(await server.execute()).toEqual({ outcome: "completed" });
      expect(server.output()).toEqual([10, 11, { flowRunId: "trn-wf" }]);
      expect(
        server.inline("start").map((s) => [s.step_key, s.task_name, unb64(s.input ?? "")]),
      ).toEqual([
        [{ seq: 0 }, "double", [5]],
        [{ seq: 1 }, "plusOne", []],
      ]);
      expect(
        server
          .inline("complete")
          .map((c) => [
            c.session_id,
            c.key,
            c.outcome.output?.serializer,
            unb64(c.outcome.output?.data ?? ""),
          ]),
      ).toEqual([
        ["trn-wf", { seq: 0 }, 1, [10]],
        ["trn-wf", { seq: 1 }, 1, [11]],
      ]);

      server.requests.length = 0;
      await server.execute();
      expect(calls).toBe(1);
      expect(server.output()).toEqual([10, 11, { flowRunId: "trn-wf" }]);
      expect(server.paths()).toEqual(["/input", "/callback"]);
    });

    it("returns what a replay would, not the live value", async () => {
      flow({ name: "wf" }, async (ctx) => {
        const value = await ctx.step("obj", () => ({ n: 1, skip: undefined }));
        return value;
      });
      await serve("wf");
      await server.execute();
      expect(server.output()).toEqual({ n: 1 });
    });

    it("accepts a plain object from another realm", async () => {
      flow({ name: "wf" }, async (ctx) => ctx.step("obj", () => runInNewContext("({ n: 1 })")));
      await serve("wf");
      await server.execute();
      expect(server.output()).toEqual({ n: 1 });
    });

    it("accepts an undefined step result and replays it", async () => {
      let calls = 0;
      flow({ name: "wf" }, async (ctx) => {
        const value = await ctx.step("void", () => {
          calls++;
        });
        return value === undefined;
      });
      await serve("wf");
      await server.execute();
      expect(server.output()).toBe(true);
      await server.execute();
      expect(server.output()).toBe(true);
      expect(calls).toBe(1);
    });

    it.each([
      ["a BigInt", 1n, "BigInt"],
      ["NaN", Number.NaN, "NaN"],
      ["a Date", new Date(0), "Date"],
      ["a class instance", new (class Order {})(), "Order"],
      ["a nested Date", { at: [new Date(0)] }, "Date"],
      ["a function", () => 1, "function"],
      ["a function property", { cb: () => 1 }, "function"],
      ["a function in an array", [() => 1], "function"],
      ["a symbol", Symbol("value"), "symbol"],
      ["a symbol property", { value: Symbol("value") }, "symbol"],
      ["a symbol in an array", [Symbol("value")], "symbol"],
      ["undefined in an array", [undefined, 1], "undefined"],
      ["undefined in a nested array", { values: [undefined, 1] }, "undefined"],
      ["a sparse array", new Array(1), "undefined"],
    ])("fails a step that returns %s without retrying it", async (_, result, message) => {
      let calls = 0;
      function step() {
        calls++;
        return result;
      }
      flow({ name: "wf" }, async (ctx) => {
        try {
          await ctx.step("step", step, [], { retry: { maxRetries: 2, waitDurationMs: 0 } });
        } catch (e) {
          return [(e as StepError).errorName, (e as StepError).message];
        }
      });
      await serve("wf");
      await server.execute();
      expect(calls).toBe(1);
      expect(server.inline("attempt")).toHaveLength(0);
      expect(server.output()).toEqual(["TypeError", expect.stringContaining(message)]);
    });

    describe.each([false, true])("argument encoding with replay=%s", (replay) => {
      it.each([
        { kind: "BigInt", value: () => 1n, cause: "BigInt" },
        {
          kind: "circular",
          value: () => {
            const value: unknown[] = [];
            value.push(value);
            return value;
          },
          cause: CIRCULAR_ENCODING_RE,
        },
      ])("fails the workflow for $kind arguments even if caught", async ({ value, cause }) => {
        const fn = vi.fn((arg: unknown) => arg);
        flow({ name: "wf" }, async (ctx) => {
          try {
            return await ctx.step("encode-args", fn, [value()], {
              retry: { maxRetries: 2, waitDurationMs: 0 },
            });
          } catch {
            return "swallowed";
          }
        });
        await serve("wf");
        if (replay) {
          server.attempt = 1;
          server.steps.set(0, {
            step_key: { seq: 0 },
            type: "inline",
            task_name: "encode-args",
            workflow_attempt: 0,
            input: b64([1]),
            output: b64([1]),
            started_at: new Date().toISOString(),
            completed_at: new Date().toISOString(),
          });
        }

        const { error } = await server.execute();
        expect(error).toBeInstanceOf(FlowFailedError);
        expect(server.lastCallback().error?.details).toContain('Arguments for step "encode-args"');
        expect(server.lastCallback().error?.details).toMatch(cause);
        expect(server.lastCallback().complete).toBeUndefined();
        expect(fn).not.toHaveBeenCalled();
        expect(server.inline("start")).toEqual([]);
        expect(server.inline("attempt")).toEqual([]);
        expect(server.inline("complete")).toEqual([]);
      });
    });

    it("gives the step a copy of its arguments", async () => {
      flow({ name: "wf" }, async (ctx) => {
        const order = { items: [1] };
        await ctx.step("mutate", (o: { items: number[] }) => o.items.push(2), [order]);
        return order;
      });
      await serve("wf");
      await server.execute();
      expect(server.output()).toEqual({ items: [1] });
    });

    it("retries in-process and records each failed attempt", async () => {
      let calls = 0;
      function flaky() {
        calls++;
        if (calls < 3) throw new Error(`fail ${calls}`);
        return "ok";
      }
      flow({ name: "wf" }, (ctx) =>
        ctx.step("flaky", flaky, [], { retry: { maxRetries: 3, waitDurationMs: 0 } }),
      );
      await serve("wf");
      await server.execute();

      expect(server.output()).toBe("ok");
      expect(server.inline("attempt").map((a) => [a.attempt, a.error?.message])).toEqual([
        [0, "fail 1"],
        [1, "fail 2"],
      ]);
      expect(server.inline("complete")).toHaveLength(1);
    });

    it("sends when each retry is due and waits until then", async () => {
      const now = Date.parse("2026-01-02T03:04:05.000Z");
      vi.spyOn(Date, "now").mockReturnValue(now);
      const waits: number[] = [];
      const setTimeout = globalThis.setTimeout;
      vi.spyOn(globalThis, "setTimeout").mockImplementation((callback, ms, ...args) => {
        waits.push(ms ?? 0);
        return setTimeout(callback, 0, ...args);
      });
      function failing(): never {
        throw new Error("down");
      }
      flow({ name: "wf" }, (ctx) =>
        ctx.step("failing", failing, [], {
          retry: { maxRetries: 2, waitDurationMs: 100, backoffScaling: 2 },
        }),
      );
      await serve("wf");
      await server.execute();

      expect(server.inline("attempt").map((a) => [a.attempt, a.retry_at])).toEqual([
        [0, "2026-01-02T03:04:05.100Z"],
        [1, "2026-01-02T03:04:05.200Z"],
      ]);
      expect(waits).toEqual(expect.arrayContaining([100, 200]));
      // The final attempt completes the step instead, with no retry to schedule.
      expect(server.inline("complete")).toHaveLength(1);
      expect(server.inline("complete")[0]?.outcome.final_attempt?.attempt).toBe(2);
    });

    it("records an exhausted step's error and rethrows it on replay", async () => {
      let calls = 0;
      class PaymentError extends Error {
        code = "card_declined";
        name = "PaymentError";
      }
      function charge(): never {
        calls++;
        throw new PaymentError("declined");
      }
      flow({ name: "wf" }, async (ctx) => {
        try {
          await ctx.step("charge", charge, [], { retry: { maxRetries: 1, waitDurationMs: 0 } });
        } catch (e) {
          const err = e as StepError;
          return [err instanceof StepError, err.errorName, err.message, (err.data as any)?.code];
        }
      });
      await serve("wf");
      await server.execute();
      const expected = [true, "PaymentError", "declined", "card_declined"];
      expect(server.output()).toEqual(expected);
      expect(calls).toBe(2);
      // The last failure ends the step as its final attempt, after attempt 0.
      const final = server.inline("complete")[0]?.outcome.final_attempt;
      expect(final?.attempt).toBe(1);
      expect(final?.data).toBeUndefined();
      expect(unb64(final?.error.data ?? "")).toMatchObject({
        name: "PaymentError",
        message: "declined",
      });
      expect(server.stepAttempts.map((a) => a.attempt)).toEqual([0, 1]);

      await server.execute();
      expect(server.output()).toEqual(expected);
      expect(calls).toBe(2);
    });

    it("continues attempt numbering from history after a crash", async () => {
      let calls = 0;
      function flaky() {
        calls++;
        throw new Error("again");
      }
      flow({ name: "wf" }, async (ctx) => {
        try {
          return await ctx.step("flaky", flaky, [], {
            retry: { maxRetries: 2, waitDurationMs: 0 },
          });
        } catch (e) {
          return (e as Error).message;
        }
      });
      await serve("wf");
      server.attempt = 1;
      server.steps.set(0, {
        step_key: { seq: 0 },
        type: "inline",
        task_name: "flaky",
        workflow_attempt: 0,
        input: b64([]),
        started_at: new Date().toISOString(),
      });
      server.stepAttempts.push({
        step_key: { seq: 0 },
        attempt: 0,
        workflow_attempt: 0,
        error: { name: "Error", message: "first" },
        ended_at: new Date().toISOString(),
      });

      await server.execute();
      expect(server.inline("start")).toHaveLength(0);
      expect(server.inline("attempt").map((a) => a.attempt)).toEqual([1]);
      expect(calls).toBe(2);
      expect(server.output()).toBe("again");
      expect(server.steps.get(0)?.workflow_attempt).toBe(1);
    });

    it("records the workflow attempt that completed a step, not the one that started it", async () => {
      let calls = 0;
      function work() {
        calls++;
        return "ok";
      }
      flow({ name: "wf" }, (ctx) =>
        ctx.step("work", work, [], { retry: { maxRetries: 1, waitDurationMs: 0 } }),
      );
      await serve("wf");
      server.attempt = 2;
      server.steps.set(0, {
        step_key: { seq: 0 },
        type: "inline",
        task_name: "work",
        workflow_attempt: 0,
        input: b64([]),
        started_at: new Date().toISOString(),
      });

      await server.execute();
      expect(calls).toBe(1);
      const outcome = server.inline("complete")[0]?.outcome;
      expect(outcome?.final_attempt).toBeUndefined();
      expect(unb64(outcome?.output?.data ?? "")).toEqual(["ok"]);
      expect(server.steps.get(0)?.workflow_attempt).toBe(2);
    });

    it("fails the run with the last recorded error when retries ran out before a crash", async () => {
      const fn = vi.fn(function step() {
        return 1;
      });
      flow({ name: "wf" }, async (ctx) => {
        try {
          return await ctx.step("step", fn, []);
        } catch {
          return "swallowed";
        }
      });
      await serve("wf");
      server.attempt = 1;
      server.steps.set(0, {
        step_key: { seq: 0 },
        type: "inline",
        task_name: "step",
        workflow_attempt: 0,
        input: b64([]),
        started_at: new Date().toISOString(),
      });
      const recorded: StepAttemptRecord = {
        step_key: { seq: 0 },
        attempt: 0,
        workflow_attempt: 0,
        error: { name: "Error", message: "recorded" },
        started_at: new Date().toISOString(),
        ended_at: new Date().toISOString(),
      };
      server.stepAttempts.push(recorded);

      const { error } = await server.execute();
      expect(fn).not.toHaveBeenCalled();
      expect(error).toBeInstanceOf(FlowFailedError);
      expect(server.lastCallback().error?.details).toContain("past its 0 retries");
      // The step completes at a new attempt number with the recorded error.
      const final = server.inline("complete")[0]?.outcome.final_attempt;
      expect(final?.attempt).toBe(1);
      expect(unb64(final?.error.data ?? "")).toEqual(recorded.error);
      expect(server.steps.get(0)?.completed_at).toBeDefined();
    });

    it("counts an attempt cut off by a crash toward the step's retries", async () => {
      let calls = 0;
      function flaky() {
        calls++;
        if (calls === 1) throw new Error("again");
        return "ok";
      }
      flow({ name: "wf" }, (ctx) =>
        ctx.step("flaky", flaky, [], { retry: { maxRetries: 2, waitDurationMs: 0 } }),
      );
      await serve("wf");
      server.attempt = 1;
      server.steps.set(0, {
        step_key: { seq: 0 },
        type: "inline",
        task_name: "flaky",
        workflow_attempt: 0,
        input: b64([]),
        started_at: new Date().toISOString(),
      });

      await server.execute();
      expect(server.output()).toBe("ok");
      expect(calls).toBe(2);
      // A crash cut off attempt 0, so replay runs attempts 1 and 2.
      expect(server.inline("attempt").map((a) => a.attempt)).toEqual([1]);
    });

    it("fails the run when a crash cut off the step's last attempt, even if caught", async () => {
      const fn = vi.fn(function step() {
        return 1;
      });
      flow({ name: "wf" }, async (ctx) => {
        try {
          return await ctx.step("step", fn, []);
        } catch {
          return "swallowed";
        }
      });
      await serve("wf");
      server.attempt = 1;
      server.steps.set(0, {
        step_key: { seq: 0 },
        type: "inline",
        task_name: "step",
        workflow_attempt: 0,
        input: b64([]),
        started_at: new Date().toISOString(),
      });

      const { error } = await server.execute();
      expect(fn).not.toHaveBeenCalled();
      expect(error).toBeInstanceOf(FlowFailedError);
      expect(server.lastCallback().error?.details).toContain("past its 0 retries");
      const final = server.inline("complete")[0]?.outcome.final_attempt;
      expect(final?.attempt).toBe(1);
      expect(unb64(final?.error.data ?? "")).toMatchObject({ name: "FlowFailedError" });
      expect(server.steps.get(0)?.completed_at).toBeDefined();
    });

    it("adopts the outcome that won when another writer completed first", async () => {
      flow({ name: "wf" }, (ctx) => ctx.step("race", () => "mine"));
      await serve("wf");
      server.beforeInline = (kind, body) => {
        const row = server.steps.get(body.key?.seq);
        if (kind === "complete" && row) {
          row.completed_at = new Date().toISOString();
          row.output = b64(["theirs"]);
        }
      };
      await server.execute();
      expect(server.output()).toBe("theirs");
    });
  });

  describe("call rules", () => {
    it("rejects parallel steps", async () => {
      flow({ name: "wf" }, (ctx) => Promise.all([ctx.step("a", () => 1), ctx.step("b", () => 2)]));
      await serve("wf");
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(ONE_STEP_RE);
    });

    it("fails the run on a ctx call from inside an inline step", async () => {
      const inner = vi.fn(() => 1);
      flow({ name: "wf" }, async (ctx) => {
        try {
          await ctx.step("nested", () => ctx.step("inner", inner), {
            retry: { maxRetries: 3, waitDurationMs: 0 },
          });
        } catch {
          return "caught";
        }
      });
      await serve("wf");
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(WITHIN_STEP_RE);
      expect(inner).not.toHaveBeenCalled();
      // The outer step isn't retried, and its failure isn't recorded.
      expect(server.stepAttempts).toEqual([]);
      expect(server.inline("complete")).toEqual([]);
    });

    it("doesn't record a step that caught its own nested ctx call", async () => {
      flow({ name: "wf" }, (ctx) =>
        ctx.step("nested", () => {
          try {
            ctx.step("inner", () => 1);
          } catch {
            // Swallowed by the step, but the run still fails.
          }
          return "done";
        }),
      );
      await serve("wf");
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(WITHIN_STEP_RE);
      expect(server.inline("complete")).toEqual([]);
    });

    it("doesn't retry a step whose delayed ctx call stopped the run", async () => {
      const outer = vi.fn();
      let release = () => {};
      const released = new Promise<void>((resolve) => {
        release = resolve;
      });
      flow({ name: "wf" }, (ctx) =>
        ctx.step(
          "nested",
          () => {
            outer();
            // Registered inside the step, so it still runs as part of it.
            released.then(() => ctx.step("inner", () => 1)).catch(() => {});
            throw new Error("boom");
          },
          { retry: { maxRetries: 3, waitDurationMs: 0 } },
        ),
      );
      await serve("wf");
      // The nested call lands while the failed attempt is being recorded.
      server.beforeInline = (kind) => {
        if (kind === "attempt") {
          release();
        }
      };
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(WITHIN_STEP_RE);
      expect(outer).toHaveBeenCalledTimes(1);
      expect(server.inline("complete")).toEqual([]);
    });

    it("requires the step's name first", async () => {
      flow({ name: "wf" }, (ctx) => (ctx.step as any)(() => 1));
      await serve("wf");
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(NAME_FIRST_RE);
    });

    it("rejects an empty step name", async () => {
      flow({ name: "wf" }, (ctx) => ctx.step("", () => 1));
      await serve("wf");
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(EMPTY_NAME_RE);
    });

    it("points ctx.invoke at ctx.step when given a function", async () => {
      flow({ name: "wf" }, (ctx) => (ctx.invoke as any)(() => 1));
      await serve("wf");
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(USE_STEP_RE);
    });

    it("points ctx.step at ctx.invoke when given a task", async () => {
      const invoice = task({ name: "invoice" }, () => 1);
      flow({ name: "wf" }, (ctx) => (ctx.step as any)("invoice", invoice));
      await serve("wf");
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(USE_INVOKE_RE);
    });
  });

  describe("determinism", () => {
    function recorded(row: Partial<StepRecord>): void {
      server.attempt = 1;
      server.steps.set(0, {
        step_key: { seq: 0 },
        type: "inline",
        task_name: "lookup",
        workflow_attempt: 0,
        input: b64(["a"]),
        output: b64(["recorded"]),
        started_at: new Date().toISOString(),
        completed_at: new Date().toISOString(),
        ...row,
      });
    }

    function lookup(key: string) {
      return key;
    }

    it("matches inputs regardless of key order", async () => {
      flow({ name: "wf" }, (ctx) => ctx.step("lookup", lookup, [{ b: 1, a: 2 } as any]));
      await serve("wf");
      recorded({ input: b64([{ a: 2, b: 1 }]) });
      await server.execute();
      expect(server.output()).toBe("recorded");
    });

    it("catches a change past the length shown in the error message", async () => {
      // The error's expected/actual text is cut off, but the comparison isn't.
      const prefix = "a".repeat(1000);
      flow({ name: "wf" }, (ctx) => ctx.step("lookup", lookup, [`${prefix}new`]));
      await serve("wf");
      recorded({ input: b64([`${prefix}old`]) });
      await server.execute();

      const determinism = server.lastCallback().error?.determinism;
      expect(determinism?.kind).toBe("input_hash");
      expect(determinism?.expected).toBe(determinism?.actual);
    });

    it("fails the run when a step's input changed, even if the error is caught", async () => {
      flow({ name: "wf" }, async (ctx) => {
        try {
          await ctx.step("lookup", lookup, ["b"]);
        } catch {
          return "swallowed";
        }
      });
      await serve("wf");
      recorded({});
      const { error } = await server.execute();

      expect(error).toBeDefined();
      const callback = server.lastCallback().error;
      expect(callback?.reason).toBe("DeterminismError");
      expect(callback?.determinism).toMatchObject({
        step_key: { seq: 0 },
        kind: "input_hash",
        expected: 'inline lookup("a")',
        actual: 'inline lookup("b")',
      });
    });

    it("fails the run when a step's type changed", async () => {
      flow({ name: "wf" }, (ctx) => ctx.step("lookup", lookup, ["a"]));
      await serve("wf");
      recorded({ type: "sleep", task_name: "", input: b64(1000) });
      await server.execute();
      expect(server.lastCallback().error?.determinism?.kind).toBe("type");
    });

    it("fails the run on an unknown step type", async () => {
      flow({ name: "wf" }, (ctx) => ctx.step("lookup", lookup, ["a"]));
      await serve("wf");
      recorded({ type: "signal" });
      await server.execute();
      expect(server.lastCallback().error?.determinism?.kind).toBe("unknown_type");
    });

    it("reports an open step's latest recorded workflow attempt", async () => {
      flow({ name: "wf" }, (ctx) => ctx.step("lookup", lookup, ["b"]));
      await serve("wf");
      recorded({ output: undefined, completed_at: undefined });
      server.attempt = 3;
      server.stepAttempts.push({
        step_key: { seq: 0 },
        attempt: 0,
        workflow_attempt: 2,
        error: { name: "Error", message: "first" },
        ended_at: new Date().toISOString(),
      });
      await server.execute();
      expect(server.lastCallback().error?.determinism?.workflow_attempt).toBe(2);
    });

    it("leaves out the workflow attempt for an open step with no recorded attempts", async () => {
      flow({ name: "wf" }, (ctx) => ctx.step("lookup", lookup, ["b"]));
      await serve("wf");
      recorded({ output: undefined, completed_at: undefined });
      await server.execute();
      const determinism = server.lastCallback().error?.determinism;
      expect(determinism?.kind).toBe("input_hash");
      expect(determinism?.workflow_attempt).toBeUndefined();
    });
  });

  describe("ctx.invoke", () => {
    it("fails the run as not supported yet", async () => {
      const invoice = task({ name: "invoice" }, (_ctx, id: string) => id);
      flow({ name: "wf" }, (ctx) => ctx.invoke(invoice, ["o-1"]));
      await serve("wf");
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(INVOKE_UNSUPPORTED_RE);
      expect(server.paths()).toEqual(["/input", "/callback"]);
    });

    it("rejects a workflow passed to ctx.invoke", async () => {
      const inner = flow({ name: "inner" }, () => 1);
      flow({ name: "wf" }, (ctx) => (ctx as any).invoke(inner));
      await serve("wf");
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(NESTED_WORKFLOW_RE);
    });
  });

  describe("ctx.sleep", () => {
    it("fails the run as not supported yet", async () => {
      flow({ name: "wf" }, (ctx) => (ctx as any).sleep(1000));
      await serve("wf");
      await server.execute();
      expect(server.lastCallback().error?.details).toMatch(SLEEP_UNSUPPORTED_RE);
      expect(server.paths()).toEqual(["/input", "/callback"]);
    });
  });

  describe("socket errors", () => {
    describe("failed-step completion over the real socket", () => {
      beforeEach(() => {
        // Exercise all transport attempts, shortening only their backoff.
        const setTimeout = globalThis.setTimeout;
        vi.spyOn(globalThis, "setTimeout").mockImplementation((callback, _ms, ...args) =>
          setTimeout(callback, 0, ...args),
        );
        vi.spyOn(console, "error").mockImplementation(() => {});
        vi.spyOn(console, "warn").mockImplementation(() => {});
      });

      it.each([false, true])(
        "waits for acknowledgement before returning the error (caught=%s)",
        async (caught) => {
          const failing = vi.fn(() => {
            throw new Error("dependency unavailable");
          });
          const fallback = vi.fn(() => "recovered");
          flow({ name: "wf" }, async (ctx) => {
            try {
              return await ctx.step("failing", failing);
            } catch (error) {
              if (!caught || !(error instanceof StepError)) throw error;
              return ctx.step("fallback", fallback);
            }
          });
          await serve("wf");
          server.inject.set("/step-inline/complete", {
            status: 500,
            body: { message: "history unavailable" },
            remaining: 2,
          });
          server.beforeInline = (kind, body) => {
            if (kind === "start" && body.step_key.seq === 1) {
              expect(server.steps.get(0)?.completed_at).toBeDefined();
            }
          };

          const result = await server.execute();
          const completions = server.inline("complete").filter((body) => body.key.seq === 0);
          expect(completions).toHaveLength(3);
          expect(completions).toEqual(new Array(3).fill(completions[0]));
          expect(failing).toHaveBeenCalledTimes(1);
          expect(server.callbacks).toHaveLength(1);
          if (caught) {
            expect(result).toEqual({ outcome: "completed" });
            expect(fallback).toHaveBeenCalledTimes(1);
            expect(server.output()).toBe("recovered");
          } else {
            expect(result.error).toBeInstanceOf(StepError);
            expect(fallback).not.toHaveBeenCalled();
            expect(server.lastCallback().error?.details).toBe("dependency unavailable");
            expect(server.lastCallback().error?.reason).toBeUndefined();
          }
        },
      );

      it.each([false, true])(
        "ends the attempt after transport retries (callback fails=%s)",
        async (rejectCallback) => {
          const failing = vi.fn(() => {
            throw new Error("dependency unavailable");
          });
          const fallback = vi.fn(() => "recovered");
          flow({ name: "wf" }, async (ctx) => {
            try {
              return await ctx.step("failing", failing);
            } catch {
              return ctx.step("fallback", fallback);
            }
          });
          await serve("wf");
          server.inject.set("/step-inline/complete", {
            status: 500,
            body: { message: "history unavailable" },
            remaining: 25,
          });
          if (rejectCallback) {
            server.inject.set("/callback", {
              status: 500,
              body: { message: "callback unavailable" },
              remaining: 25,
            });
          }

          const result = await server.execute();
          expect(result.error).toBeInstanceOf(UnreportedError);
          expect(failing).toHaveBeenCalledTimes(1);
          expect(fallback).not.toHaveBeenCalled();
          const completions = server.inline("complete");
          expect(completions).toHaveLength(25);
          expect(completions).toEqual(new Array(25).fill(completions[0]));
          expect(server.steps.get(0)?.completed_at).toBeUndefined();
          const callbacks = server.requests.filter((request) => request.path === "/callback");
          expect(callbacks).toHaveLength(rejectCallback ? 25 : 1);
          for (const callback of callbacks) {
            expect(callback.body.error.reason).toBe("system_error");
            expect(callback.body.error.details).toContain("history unavailable");
          }
        },
      );
    });

    it("fails the run on a limit error", async () => {
      flow({ name: "wf" }, (ctx) => ctx.step("big", () => 1));
      await serve("wf");
      server.inject.set("/step-inline/start", {
        status: 422,
        body: { code: "workflow_payload_too_large", message: "too big", limit: 10, value: 11 },
      });
      await server.execute();
      expect(server.lastCallback().error).toMatchObject({
        details: expect.stringMatching(HTTP_422_RE),
        reason: "workflow_payload_too_large",
        limit: 10,
        value: 11,
      });
    });

    it("stops without a callback when the run was cancelled", async () => {
      flow({ name: "wf" }, (ctx) => ctx.step("step", () => 1));
      await serve("wf");
      server.inject.set("/step-inline/start", {
        status: 409,
        body: { code: "run_cancelled", message: "cancelled" },
      });
      expect(await server.execute()).toEqual({ outcome: "stopped" });
      expect(server.callbacks).toHaveLength(0);
    });

    describe("when the socket can't be reached", () => {
      beforeEach(() => {
        // The client's own retries take minutes, so fail the request outright.
        vi.spyOn(UDSClient.prototype, "stepStart").mockRejectedValue(new Error("connect ENOENT"));
        vi.spyOn(console, "error").mockImplementation(() => {});
        vi.spyOn(console, "warn").mockImplementation(() => {});
      });

      it("reports a system error, then exits", async () => {
        flow({ name: "wf" }, (ctx) => ctx.step("step", () => 1));
        await serve("wf");

        const { error } = await server.execute();
        expect(error).toBeInstanceOf(UnreportedError);
        expect(server.callbacks).toEqual([
          { error: { details: "connect ENOENT", reason: "system_error" } },
        ]);
      });

      it("still exits when the callback fails", async () => {
        flow({ name: "wf" }, (ctx) => ctx.step("step", () => 1));
        await serve("wf");
        vi.spyOn(UDSClient.prototype, "sendCallback").mockRejectedValue(
          new Error("HTTP 500: down"),
        );

        const { error } = await server.execute();
        expect(error).toBeInstanceOf(UnreportedError);
        expect(console.warn).toHaveBeenCalled();
      });
    });
  });
});

describe("FlowContext types", () => {
  it("types ctx.invoke and ctx.step by their target", () => {
    const invoice = task({ name: "typesInvoice" }, (_ctx, id: string, cents: number) => ({
      id,
      cents,
    }));
    const ping = task({ name: "typesPing" }, () => "pong");
    function charge(id: string, total: number) {
      return { id, total };
    }

    flow({ name: "typesWf" }, async (ctx) => {
      expectTypeOf(await ctx.invoke(invoice, ["o", 1])).toEqualTypeOf<{
        id: string;
        cents: number;
      }>();
      expectTypeOf(await ctx.invoke(ping)).toEqualTypeOf<string>();
      expectTypeOf(
        await ctx.step("charge", charge, ["o", 1], { retry: { maxRetries: 1, waitDurationMs: 0 } }),
      ).toEqualTypeOf<{
        id: string;
        total: number;
      }>();
      expectTypeOf(await ctx.step("n", async () => 1)).toEqualTypeOf<number>();

      // @ts-expect-error ctx.invoke takes no options at GA
      await ctx.invoke(invoice, ["o", 1], { retry: { maxRetries: 1, waitDurationMs: 0 } });
      // @ts-expect-error wrong argument types
      await ctx.step("charge", charge, [1, "o"]);
      // @ts-expect-error a task's arguments go in an array
      await ctx.invoke(invoice, "o", 1);
      // @ts-expect-error ctx.invoke takes a task, not a function
      await ctx.invoke(charge, ["o", 1]);
      // @ts-expect-error ctx.step takes the step's name first
      await ctx.step(charge, ["o", 1]);
      // @ts-expect-error ctx.step takes a function, not a task
      await ctx.step("invoice", invoice, ["o", 1]);
    });

    // Type checks only: these are never called.
    const retry = { maxRetries: 1, waitDurationMs: 0 };
    const taskOptions: RegisterTaskOptions = { name: "typesTaskOptions", retry };
    const _registrations = [
      // @ts-expect-error workflows take no retry policy
      () => flow({ name: "typesRetry", retry }, () => 1),
      // @ts-expect-error task options may carry a retry policy, so they aren't workflow options
      () => flow(taskOptions, () => 1),
    ];
  });
});
