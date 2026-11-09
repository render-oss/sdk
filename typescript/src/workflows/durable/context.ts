import { AsyncLocalStorage } from "node:async_hooks";
import { createHash } from "node:crypto";
import { RenderError } from "../../errors.js";
import { canonicalJson, decodeArgs, decodeOutput, encodeArgs, encodeOutput } from "../encoding.js";
import { TaskRegistry } from "../registry.js";
import type {
  FlowContext,
  FlowRunMetadata,
  GetInputResponse,
  Payload,
  Retry,
  StepAttemptRecord,
  StepKey,
  StepOptions,
  StepOutcome,
  StepRecord,
  TaskDefinition,
  TaskErrorBody,
  WireStepError,
} from "../types.js";
import { SocketHttpError, type UDSClient } from "../uds.js";
import { DeterminismError, FlowFailedError, StepError, WorkflowLimitError } from "./errors.js";

type StepType = "inline" | "invoked";

const STEP_TYPES = new Set<string>(["inline", "invoked", "sleep"]);
const DEFAULT_BACKOFF_SCALING = 1.5;
const DESCRIPTION_LIMIT = 500;
const JSON_SERIALIZER = 1;

/** Why a workflow attempt stopped before its function settled. */
export type FlowHalt =
  /** Suspended while an invoked task runs. The process will be stopped. */
  | { kind: "suspended" }
  /** The run was cancelled. Stop without reporting anything. */
  | { kind: "cancelled" }
  /** The run fails, and a replay would fail the same way. */
  | { kind: "failed"; error: DeterminismError | FlowFailedError }
  /** The socket couldn't be reached. Report a system error if possible and exit, so the run recovers. */
  | { kind: "unreachable"; error: Error };

/** A recorded outcome: an output, or an error to rethrow. */
interface Outcome {
  output?: string;
  error?: WireStepError;
}

/** The failed attempt that ends an inline step. */
interface FinalAttempt {
  attempt: number;
  startedAt: string;
  endedAt: string;
  error: WireStepError;
}

function jsonPayload(data: string): Payload {
  return data ? { serializer: JSON_SERIALIZER, data } : { serializer: JSON_SERIALIZER };
}

/**
 * Encode a step error as a JSON payload. Keys are sorted, so a recorded
 * attempt sent again as the final attempt encodes to the same bytes.
 */
function errorPayload(error: WireStepError): Payload {
  return jsonPayload(Buffer.from(canonicalJson(error)).toString("base64"));
}

function never<T>(): Promise<T> {
  return new Promise<T>(() => {});
}

function delay(ms: number): Promise<void> {
  return ms > 0 ? new Promise((resolve) => setTimeout(resolve, ms)) : Promise.resolve();
}

function backoffMs(retry: Retry | undefined, failedAttempt: number): number {
  if (!retry) {
    return 0;
  }
  return retry.waitDurationMs * (retry.backoffScaling ?? DEFAULT_BACKOFF_SCALING) ** failedAttempt;
}

/** Give a step its own copy of its arguments, so it can't mutate the workflow's. */
function isolate(args: unknown[]): unknown[] {
  try {
    return structuredClone(args);
  } catch {
    return args;
  }
}

function isTaskDefinition(target: unknown): target is TaskDefinition & { flow?: boolean } {
  return (
    typeof target === "object" &&
    target !== null &&
    typeof (target as TaskDefinition).name === "string" &&
    typeof (target as TaskDefinition).func === "function"
  );
}

/** A readable form of a call for error messages. Truncated, so never compare it. */
function describeCall(type: StepType | string, name: string, inputJson: string): string {
  const call =
    type === "sleep" ? `sleep(${inputJson}ms)` : `${type} ${name}(${inputJson.slice(1, -1)})`;
  return call.length > DESCRIPTION_LIMIT ? `${call.slice(0, DESCRIPTION_LIMIT)}…` : call;
}

/**
 * What replay compares: a hash of the step's name and its full canonical
 * input. The name is JSON-encoded so the boundary between the two parts is
 * unambiguous.
 */
function inputHash(name: string, inputJson: string): string {
  return createHash("sha256").update(JSON.stringify(name)).update(inputJson).digest("hex");
}

/**
 * The {@link FlowContext} handed to a workflow. It numbers each `ctx`
 * call, matches it against the run's recorded history, and records new
 * steps through the socket.
 */
export class DurableFlowContext implements FlowContext {
  readonly metadata: FlowRunMetadata;
  /** Settles when the attempt stops before the workflow function settles. */
  readonly halted: Promise<FlowHalt>;

  private haltReason?: FlowHalt;
  private resolveHalted!: (halt: FlowHalt) => void;
  private readonly steps = new Map<number, StepRecord>();
  private readonly attempts = new Map<number, StepAttemptRecord[]>();
  /** Identifies this run's step history. renderd checks it on each completion. */
  private readonly sessionId: string;
  private nextSeq = 0;
  private inFlight = false;
  /** The name of the inline step whose function is running, inside that function. */
  private readonly runningStep = new AsyncLocalStorage<string>();

  constructor(
    private readonly udsClient: UDSClient,
    input: GetInputResponse,
  ) {
    this.sessionId = input.task_run_id ?? "";
    this.metadata = { flowRunId: this.sessionId };
    for (const step of input.history?.steps ?? []) {
      this.steps.set(step.step_key.seq, step);
    }
    for (const attempt of input.history?.step_attempts ?? []) {
      const list = this.attempts.get(attempt.step_key.seq) ?? [];
      list.push(attempt);
      this.attempts.set(attempt.step_key.seq, list);
    }
    this.halted = new Promise((resolve) => {
      this.resolveHalted = resolve;
    });
  }

  /** Why the attempt stopped, once it has. */
  get halt(): FlowHalt | undefined {
    return this.haltReason;
  }

  invoke(task: TaskDefinition<any[], any>, args?: unknown[]): Promise<any> {
    if (!isTaskDefinition(task)) {
      throw new RenderError(
        typeof task === "function"
          ? "ctx.invoke takes a registered task; use ctx.step to run a function"
          : "ctx.invoke takes a registered task",
      );
    }
    if (task.flow) {
      throw new RenderError(
        `ctx.invoke(${task.name}): a workflow can't run another workflow; run a task instead`,
      );
    }
    if (!TaskRegistry.getInstance().has(task.name)) {
      throw new RenderError(`Task '${task.name}' is not registered`);
    }
    const taskArgs = args ?? [];
    if (!Array.isArray(taskArgs)) {
      throw new RenderError(
        `ctx.invoke(${task.name}, ...): pass the task's arguments as an array, such as [a, b]`,
      );
    }
    throw new RenderError(
      `ctx.invoke(${task.name}): invoking a registered task from a workflow isn't supported yet`,
    );
  }

  // Not on FlowContext yet, so a call fails with this error, not a TypeError.
  sleep(..._args: unknown[]): Promise<never> {
    throw new RenderError("ctx.sleep: sleeping in a flow isn't supported yet");
  }

  step(
    name: string,
    fn: (...args: any[]) => unknown,
    argsOrOptions?: unknown[] | StepOptions,
    options?: StepOptions,
  ): Promise<any> {
    if (typeof name !== "string") {
      throw new RenderError(
        `ctx.step takes the step's name first, such as ctx.step("charge", charge, [orderId])`,
      );
    }
    if (!name) {
      throw new RenderError("ctx.step needs a non-empty step name");
    }
    if (isTaskDefinition(fn)) {
      throw new RenderError(
        `ctx.step(${name}, ${fn.name}): ${fn.name} is a registered task; use ctx.invoke to run it`,
      );
    }
    if (typeof fn !== "function") {
      throw new RenderError(`ctx.step(${name}, ...) takes a function`);
    }
    // The options come third when the function takes no arguments.
    const args = Array.isArray(argsOrOptions) ? argsOrOptions : [];
    const stepOptions = Array.isArray(argsOrOptions) ? options : argsOrOptions;
    return this.nextStep((ref) => this.inlineStep(ref, name, fn, args, stepOptions?.retry));
  }

  /**
   * Take the next seq synchronously, before any await, so the numbering
   * depends only on the order of calls, then run the step.
   */
  private nextStep<T>(body: (ref: StepKey) => Promise<T>): Promise<T> {
    if (this.haltReason?.kind === "failed") {
      throw this.haltReason.error;
    }
    if (this.haltReason) {
      return never();
    }
    // Either fails the run, even if the workflow or an enclosing step catches it.
    const outerStep = this.runningStep.getStore();
    if (outerStep !== undefined) {
      const error = new FlowFailedError(
        `ctx.step can't be called within a step: step "${outerStep}" made a ctx call from its function. ` +
          "Make ctx calls from the workflow function instead.",
      );
      this.setHalt({ kind: "failed", error });
      throw error;
    }
    if (this.inFlight) {
      const error = new FlowFailedError(
        "A workflow runs one step at a time: await each ctx call before making the next. " +
          "Promise.all over ctx calls isn't currently supported.",
      );
      this.setHalt({ kind: "failed", error });
      throw error;
    }

    const seq = this.nextSeq++;
    const ref: StepKey = { seq };
    this.inFlight = true;
    return body(ref).then(
      (value) => {
        this.inFlight = false;
        return value;
      },
      (error) => {
        this.inFlight = false;
        return this.handleError(error);
      },
    );
  }

  /**
   * Pass step failures through to workflow code, and stop the attempt on
   * anything that ends it.
   */
  private handleError(error: unknown): Promise<never> {
    if (error instanceof StepError) {
      throw error;
    }
    if (error instanceof DeterminismError || error instanceof FlowFailedError) {
      return this.stop({ kind: "failed", error });
    }
    if (error instanceof SocketHttpError && error.status >= 400 && error.status < 500) {
      if (error.status === 409 && error.code !== "missing_start") {
        return this.stop({ kind: "cancelled" });
      }
      if (error.status !== 429) {
        const message = `Workflow step was rejected: ${error.message}`;
        if (error.status === 422 && error.code) {
          const { limit, value } = JSON.parse(error.body);
          const reason = error.code as TaskErrorBody["reason"];
          return this.stop({
            kind: "failed",
            error: new WorkflowLimitError(message, reason, limit, value),
          });
        }
        return this.stop({ kind: "failed", error: new FlowFailedError(message) });
      }
    }
    if (error instanceof RenderError) {
      throw error;
    }
    return this.stop({
      kind: "unreachable",
      error: error instanceof Error ? error : new Error(String(error)),
    });
  }

  private stop(halt: FlowHalt): Promise<never> {
    this.setHalt(halt);
    if (halt.kind === "failed") {
      return Promise.reject(halt.error);
    }
    return never();
  }

  private setHalt(halt: FlowHalt): void {
    if (!this.haltReason) {
      this.haltReason = halt;
      this.resolveHalted(halt);
    }
  }

  // biome-ignore lint/correctness/noUnusedPrivateClassMembers: unused until ctx.invoke is supported
  private async runInvoked(ref: StepKey, taskName: string, args: unknown[]): Promise<unknown> {
    const recorded = this.match(ref, "invoked", taskName, args);
    if (recorded?.completed_at) {
      return this.outcome(recorded);
    }

    // An open row means the child was dispatched: reattach instead.
    const childRunId = recorded
      ? recorded.child_run_id
      : await this.udsClient.runSubtask(taskName, args, ref);
    if (!childRunId) {
      throw new FlowFailedError(`Step ${ref.seq} has no recorded child run`);
    }

    const waited = await this.udsClient.stepWait({
      seq: ref.seq,
      child_run_id: childRunId,
    });
    if (waited.action === "suspending") {
      return this.stop({ kind: "suspended" });
    }
    if (waited.error) {
      throw StepError.fromTaskError(waited.error);
    }
    return decodeOutput(waited.complete?.output);
  }

  private async inlineStep(
    ref: StepKey,
    name: string,
    fn: (...args: unknown[]) => unknown,
    args: unknown[],
    retry: Retry | undefined,
  ): Promise<unknown> {
    let input: string;
    try {
      input = encodeArgs(args);
    } catch (error) {
      throw new FlowFailedError(
        `Arguments for step "${name}" can't be encoded: ${error instanceof Error ? error.message : String(error)}`,
      );
    }
    const recorded = this.match(ref, "inline", name, args);
    if (recorded?.completed_at) {
      return this.outcome(recorded);
    }

    // Failed attempts from earlier workflow attempts count toward the limit.
    // An open step with no failures lost its first attempt to a crash, so
    // count that attempt too.
    const failures = recorded ? (this.attempts.get(ref.seq) ?? []) : [];
    let attempt = recorded ? Math.max(failures.length, 1) : 0;

    if (!recorded) {
      const started = await this.udsClient.stepStart({
        step_key: ref,
        task_name: name,
        input,
        started_at: new Date().toISOString(),
      });
      if (!started.applied && started.step) {
        this.check(ref, started.step, "inline", name, args);
        if (started.step.completed_at) {
          return this.outcome(started.step);
        }
      }
    }

    const maxAttempts = (retry?.maxRetries ?? 0) + 1;
    const lastFailure = failures.at(-1);
    if (attempt >= maxAttempts) {
      return this.failResumedPastRetries(ref, name, attempt, maxAttempts - 1, lastFailure?.error);
    }
    if (lastFailure) {
      // Wait out only what's left of the backoff after the last failure.
      const elapsed = Date.now() - Date.parse(lastFailure.ended_at);
      await delay(backoffMs(retry, attempt - 1) - elapsed);
    }

    // Once the attempt has stopped, such as from a ctx call inside the step,
    // the step runs and records nothing more, even if its function caught the error.
    while (true) {
      if (this.haltReason) {
        return never();
      }
      const startedAt = new Date().toISOString();
      let value: unknown;
      try {
        value = await this.runningStep.run(name, () => fn(...isolate(args)));
        if (this.haltReason) {
          return never();
        }
      } catch (error) {
        if (this.haltReason) {
          return never();
        }
        const wireError = StepError.serialize(error);
        if (attempt + 1 >= maxAttempts) {
          return this.failInline(ref, {
            attempt,
            startedAt,
            endedAt: new Date().toISOString(),
            error: wireError,
          });
        }
        // applied: false means this attempt number is already recorded;
        // either way the next attempt takes the next number.
        await this.udsClient.stepAttempt({
          step_key: ref,
          attempt,
          error: wireError,
          started_at: startedAt,
        });
        await delay(backoffMs(retry, attempt));
        attempt++;
        continue;
      }

      let output: string;
      try {
        output = encodeOutput(value, { strict: true });
      } catch (error) {
        // Not retried: another attempt would repeat the step's side effects
        // and return a value that still can't be encoded.
        return this.failInline(ref, {
          attempt,
          startedAt,
          endedAt: new Date().toISOString(),
          error: StepError.serialize(error),
        });
      }
      return this.completeInline(
        ref,
        { completed_at: new Date().toISOString(), output: jsonPayload(output) },
        { output },
      );
    }
  }

  /**
   * Fail the run when a crash cut off a step's last attempt. Complete the step
   * at a new attempt number, with its last recorded error or else the run's
   * error, so later replays don't rerun it.
   */
  private async failResumedPastRetries(
    ref: StepKey,
    name: string,
    attempt: number,
    maxRetries: number,
    lastError?: WireStepError,
  ): Promise<never> {
    const error = new FlowFailedError(
      `ctx.step(${name}) resumed at attempt ${attempt}, past its ${maxRetries} retries`,
    );
    const now = new Date().toISOString();
    try {
      await this.failInline(ref, {
        attempt,
        startedAt: now,
        endedAt: now,
        error: lastError ?? StepError.serialize(error),
      });
    } catch (e) {
      // failInline rethrows the error as a StepError, which the flow can
      // catch. Throw the FlowFailedError instead.
      if (!(e instanceof StepError)) {
        throw e;
      }
    }
    throw error;
  }

  private failInline(ref: StepKey, final: FinalAttempt): Promise<unknown> {
    return this.completeInline(
      ref,
      {
        completed_at: final.endedAt,
        final_attempt: {
          session_id: this.sessionId,
          key: ref,
          attempt: final.attempt,
          started_at: final.startedAt,
          ended_at: final.endedAt,
          error: errorPayload(final.error),
        },
      },
      { error: final.error },
    );
  }

  /** Record a step's outcome. result is what a replay will see for it. */
  private async completeInline(
    ref: StepKey,
    outcome: StepOutcome,
    result: Outcome,
  ): Promise<unknown> {
    const completed = await this.udsClient.stepComplete({
      session_id: this.sessionId,
      key: ref,
      outcome,
    });
    // A losing write adopts the outcome that won.
    return this.outcome(!completed.applied && completed.outcome ? completed.outcome : result);
  }

  /**
   * Return a recorded output or rethrow a recorded error. A first run goes
   * through the same encoding, so it sees exactly what a replay would.
   */
  private outcome(record: Outcome): unknown {
    if (record.error) {
      throw new StepError(record.error);
    }
    return decodeOutput(record.output);
  }

  /** The recorded step for this call, after checking that it matches. */
  private match(
    ref: StepKey,
    type: StepType,
    name: string,
    input: unknown[],
  ): StepRecord | undefined {
    const recorded = this.steps.get(ref.seq);
    if (recorded) {
      this.check(ref, recorded, type, name, input);
    }
    return recorded;
  }

  private check(
    ref: StepKey,
    recorded: StepRecord,
    type: StepType,
    name: string,
    input: unknown[],
  ): void {
    const diverged = (
      kind: "input_hash" | "type" | "unknown_type",
      expected: string,
      actual: string,
    ) =>
      new DeterminismError({
        step_key: ref,
        // A step's workflow attempt is 0 until it completes, so an open step
        // reports its latest recorded attempt's, when it has one.
        workflow_attempt: recorded.completed_at
          ? recorded.workflow_attempt
          : this.attempts.get(ref.seq)?.at(-1)?.workflow_attempt,
        kind,
        expected,
        actual,
      });

    const actualJson = canonicalJson(input);
    const actual = describeCall(type, name, actualJson);
    if (!STEP_TYPES.has(recorded.type)) {
      throw diverged("unknown_type", `a step of type ${recorded.type}`, actual);
    }

    // A missing recorded input can't be compared, so only the name is checked.
    const recordedName = recorded.task_name ?? "";
    const recordedJson = recorded.input ? canonicalJson(decodeArgs(recorded.input)) : actualJson;
    const expected = describeCall(recorded.type, recordedName, recordedJson);
    if (recorded.type !== type) {
      throw diverged("type", expected, actual);
    }
    if (inputHash(recordedName, recordedJson) !== inputHash(name, actualJson)) {
      throw diverged("input_hash", expected, actual);
    }
  }
}
