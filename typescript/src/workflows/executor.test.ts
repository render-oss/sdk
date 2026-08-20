import { mkdtempSync, rmSync } from "node:fs";
import http from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { TaskExecutor } from "./executor.js";
import { TaskRegistry } from "./registry.js";
import { task } from "./task.js";
import type { CallbackRequest } from "./types.js";

/**
 * A stand-in for the workflow system, speaking the real protocol over a real
 * Unix domain socket. Exercising the executor end to end covers the wire
 * encoding as well as the call itself.
 */
class FakeWorkflowServer {
  readonly callbacks: CallbackRequest[] = [];
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
      res.setHeader("Content-Type", "application/json");
      res.end(
        JSON.stringify({
          task_name: this.taskName,
          input: Buffer.from(JSON.stringify(this.input)).toString("base64"),
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
