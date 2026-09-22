import { mkdtempSync, rmSync } from "node:fs";
import http from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { TaskExecutor } from "./executor.js";
import { TaskRegistry } from "./registry.js";
import { task } from "./task.js";
import type { CallbackRequest, GetInputResponse, TaskContext } from "./types.js";

/**
 * A stand-in for the workflow system, speaking the real protocol over a real
 * Unix domain socket. Exercising the executor end to end covers the wire
 * encoding as well as the call itself.
 */
class FakeWorkflowServer {
  readonly callbacks: CallbackRequest[] = [];
  inputRequests = 0;
  runIds: Partial<GetInputResponse> = {};
  private readonly server: http.Server;
  private readonly dir: string;
  readonly socketPath: string;

  constructor(
    private readonly taskName: string,
    private readonly input: unknown,
  ) {
    this.dir = mkdtempSync(join(tmpdir(), "rnd-"));
    this.socketPath = join(this.dir, "s.sock");
    this.server = http.createServer((req, res) => this.handle(req, res));
  }

  private handle(req: http.IncomingMessage, res: http.ServerResponse): void {
    if (req.url === "/input") {
      this.inputRequests++;
      res.setHeader("Content-Type", "application/json");
      res.end(
        JSON.stringify({
          task_name: this.taskName,
          input: Buffer.from(JSON.stringify(this.input)).toString("base64"),
          ...this.runIds,
        }),
      );
      return;
    }

    const chunks: Buffer[] = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      if (req.url === "/callback") {
        this.callbacks.push(JSON.parse(Buffer.concat(chunks).toString()));
      }
      res.end("");
    });
  }

  start(): Promise<void> {
    return new Promise((resolve) => this.server.listen(this.socketPath, resolve));
  }

  async stop(): Promise<void> {
    await new Promise((resolve) => this.server.close(resolve));
    rmSync(this.dir, { recursive: true, force: true });
  }

  /** The decoded output of the single success callback the executor sent. */
  completedOutput(): unknown {
    const [callback] = this.callbacks;
    const output = callback?.complete?.output;
    if (!output) {
      throw new Error(`no completed callback: ${JSON.stringify(this.callbacks)}`);
    }
    return JSON.parse(Buffer.from(output, "base64").toString())[0];
  }
}

async function runTask(taskName: string, input: unknown): Promise<FakeWorkflowServer> {
  const server = new FakeWorkflowServer(taskName, input);
  await server.start();
  try {
    await new TaskExecutor(server.socketPath).executeTask();
  } finally {
    await server.stop();
  }
  return server;
}

describe("TaskExecutor", () => {
  beforeEach(() => {
    TaskRegistry.getInstance().clear();
  });

  it("caches run metadata per execution using the existing input request", async () => {
    const contexts: TaskContext[] = [];
    task({ name: "recordIds" }, async (ctx) => {
      contexts.push(ctx);
      for (let i = 0; i < 3; i++) {
        await Promise.resolve();
        expect(ctx.metadata.taskRunId).toBe("trn-child");
        expect(ctx.metadata.rootTaskRunId).toBe("trn-root");
        expect(ctx.metadata.parentTaskRunId).toBe("trn-parent");
      }
    });

    const server = new FakeWorkflowServer("recordIds", []);
    server.runIds = {
      task_run_id: "trn-child",
      root_task_run_id: "trn-root",
      parent_task_run_id: "trn-parent",
    };
    await server.start();
    try {
      const executor = new TaskExecutor(server.socketPath);
      await executor.executeTask();
      expect(server.inputRequests).toBe(1);

      TaskRegistry.getInstance().clear();
      task({ name: "recordIds" }, (ctx) => {
        contexts.push(ctx);
        expect(ctx.metadata.taskRunId).toBe("trn-next");
        expect(ctx.metadata.rootTaskRunId).toBe("trn-next");
        expect(ctx.metadata.parentTaskRunId).toBeUndefined();
      });
      server.runIds = { task_run_id: "trn-next", root_task_run_id: "trn-next" };
      await executor.executeTask();
      expect(server.inputRequests).toBe(2);
      expect(contexts[0]).not.toBe(contexts[1]);
      expect(contexts[0].metadata).not.toBe(contexts[1].metadata);
      expect(contexts[0].metadata.taskRunId).toBe("trn-child");
    } finally {
      await server.stop();
    }
  });

  it.each([
    { taskRunId: "trn-root", parentTaskRunId: undefined },
    { taskRunId: "trn-child", parentTaskRunId: "trn-parent" },
  ])(
    "treats an empty root ID as unavailable for $taskRunId",
    async ({ taskRunId, parentTaskRunId }) => {
      task({ name: "emptyRoot" }, (ctx) => {
        expect(ctx.metadata.taskRunId).toBe(taskRunId);
        expect(ctx.metadata.rootTaskRunId).toBeUndefined();
        expect(ctx.metadata.parentTaskRunId).toBe(parentTaskRunId);
        return "ok";
      });

      const server = new FakeWorkflowServer("emptyRoot", []);
      server.runIds = {
        task_run_id: taskRunId,
        root_task_run_id: "",
        parent_task_run_id: parentTaskRunId,
      };
      await server.start();
      try {
        await new TaskExecutor(server.socketPath).executeTask();
        expect(server.inputRequests).toBe(1);
        expect(server.completedOutput()).toBe("ok");
      } finally {
        await server.stop();
      }
    },
  );

  it("passes a context first, then the wire input", async () => {
    const seen: unknown[] = [];
    task({ name: "record" }, (ctx, a: number, b: string) => {
      seen.push(ctx, a, b);
      return "ok";
    });

    const server = await runTask("record", [7, "hello"]);

    const [ctx, a, b] = seen;
    expect(ctx).toHaveProperty("run");
    expect(typeof (ctx as { run: unknown }).run).toBe("function");
    expect(a).toBe(7);
    expect(b).toBe("hello");
    expect(server.completedOutput()).toBe("ok");
  });

  it("does not pass the first input as the context", async () => {
    let received: unknown;
    task({ name: "firstArg" }, (ctx) => {
      received = ctx;
      return null;
    });

    await runTask("firstArg", [{ userSuppliedInput: true }]);

    expect(received).not.toEqual({ userSuppliedInput: true });
    expect(received).toHaveProperty("run");
  });

  it("gives a task with no inputs just the context", async () => {
    let argCount = -1;
    task({ name: "noInputs" }, (...args: unknown[]) => {
      argCount = args.length;
      return "done";
    });

    const server = await runTask("noInputs", []);

    expect(argCount).toBe(1);
    expect(server.completedOutput()).toBe("done");
  });

  it("awaits an async handler before reporting its result", async () => {
    task({ name: "asyncTask" }, async (_ctx, a: number) => {
      await new Promise((resolve) => setTimeout(resolve, 1));
      return a * 2;
    });

    const server = await runTask("asyncTask", [21]);

    expect(server.completedOutput()).toBe(42);
  });

  it("reports an unregistered task as an error callback", async () => {
    const server = new FakeWorkflowServer("missing", []);
    await server.start();
    try {
      await expect(new TaskExecutor(server.socketPath).executeTask()).rejects.toThrow(
        "Task 'missing' not found in registry",
      );
    } finally {
      await server.stop();
    }

    expect(server.callbacks[0]?.error?.details).toContain("not found in registry");
  });

  it("reports a thrown handler error as an error callback", async () => {
    task({ name: "boom" }, () => {
      throw new Error("handler exploded");
    });

    const server = new FakeWorkflowServer("boom", []);
    await server.start();
    try {
      await expect(new TaskExecutor(server.socketPath).executeTask()).rejects.toThrow(
        "handler exploded",
      );
    } finally {
      await server.stop();
    }

    expect(server.callbacks[0]?.error?.details).toBe("handler exploded");
  });
});
