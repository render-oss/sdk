import { RenderError } from "../errors.js";
import { WorkflowTaskContext } from "./context.js";
import { TaskRegistry } from "./registry.js";
import { task } from "./task.js";
import type { GetSubtaskResultResponse } from "./types.js";
import type { UDSClient } from "./uds.js";

/**
 * Encode a value the way the workflow system returns subtask output.
 */
function encodeOutput(value: unknown): string {
  return Buffer.from(JSON.stringify([value])).toString("base64");
}

function completed(value: unknown): GetSubtaskResultResponse {
  return { still_running: false, complete: { output: encodeOutput(value) } };
}

class FakeUDSClient {
  readonly submitted: Array<{ taskName: string; args: unknown[] }> = [];
  private nextId = 0;
  private readonly results: Map<string, GetSubtaskResultResponse[]> = new Map();

  /** Queue the sequence of poll responses returned for the next submission. */
  respondWith(...responses: GetSubtaskResultResponse[]): string {
    const id = `subtask-${this.nextId++}`;
    this.results.set(id, [...responses]);
    return id;
  }

  async runSubtask(taskName: string, args: unknown[]): Promise<string> {
    this.submitted.push({ taskName, args });
    const pending = [...this.results.keys()];
    const id = pending[this.submitted.length - 1];
    if (!id) {
      throw new Error(`no queued response for submission of '${taskName}'`);
    }
    return id;
  }

  async getSubtaskResult(subtaskId: string): Promise<GetSubtaskResultResponse> {
    const queue = this.results.get(subtaskId);
    if (!queue || queue.length === 0) {
      throw new Error(`no queued result for ${subtaskId}`);
    }
    // Hold the terminal response so repeated polls stay consistent.
    return queue.length === 1 ? queue[0] : (queue.shift() as GetSubtaskResultResponse);
  }
}

function newContext(): { context: WorkflowTaskContext; uds: FakeUDSClient } {
  const uds = new FakeUDSClient();
  return { context: new WorkflowTaskContext(uds as unknown as UDSClient), uds };
}

describe("WorkflowTaskContext", () => {
  beforeEach(() => {
    TaskRegistry.getInstance().clear();
  });

  describe("run", () => {
    it("submits the task by name and returns its decoded output", async () => {
      const { context, uds } = newContext();
      const square = task({ name: "square" }, (_ctx, a: number) => a * a);
      uds.respondWith(completed(25));

      await expect(context.run(square, 5)).resolves.toBe(25);
      expect(uds.submitted).toEqual([{ taskName: "square", args: [5] }]);
    });

    it("returns undefined when the subtask produced no output", async () => {
      const { context, uds } = newContext();
      const noop = task({ name: "noop" }, () => {});
      uds.respondWith({ still_running: false, complete: { output: "" } });

      await expect(context.run(noop)).resolves.toBeUndefined();
    });

    it("polls until the subtask finishes", async () => {
      vi.useFakeTimers();
      try {
        const { context, uds } = newContext();
        const slow = task({ name: "slow" }, () => "done");
        uds.respondWith({ still_running: true }, { still_running: true }, completed("done"));

        const pending = context.run(slow);
        await vi.advanceTimersByTimeAsync(2000);

        await expect(pending).resolves.toBe("done");
      } finally {
        vi.useRealTimers();
      }
    });

    it("surfaces the subtask error details", async () => {
      const { context, uds } = newContext();
      const failing = task({ name: "failing" }, () => "unreached");
      uds.respondWith({
        still_running: false,
        error: { details: "divide by zero" },
      });

      await expect(context.run(failing)).rejects.toThrow(
        new RenderError("Subtask failed: divide by zero"),
      );
    });

    it("forwards every argument of a variadic task", async () => {
      const { context, uds } = newContext();
      const sum = task({ name: "sum" }, (_ctx, ...values: number[]) =>
        values.reduce((a, b) => a + b, 0),
      );
      uds.respondWith(completed(6));

      await expect(context.run(sum, 1, 2, 3)).resolves.toBe(6);
      expect(uds.submitted).toEqual([{ taskName: "sum", args: [1, 2, 3] }]);
    });

    it("rejects a task that is not in the registry", async () => {
      const { context } = newContext();
      const orphan = task({ name: "orphan" }, () => 1);
      TaskRegistry.getInstance().clear();

      await expect(context.run(orphan)).rejects.toThrow("Task 'orphan' is not registered");
    });
  });
});
