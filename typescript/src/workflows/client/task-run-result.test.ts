import { TaskRunResult } from "./task-run-result.js";
import type { TaskRunDetails } from "./types.js";

const mockDetails: TaskRunDetails = {
  id: "run-123",
  status: "completed",
  taskId: "task-1",
  results: [42],
} as unknown as TaskRunDetails;

function createMockWait() {
  return vi.fn().mockResolvedValue(mockDetails);
}

describe("TaskRunResult", () => {
  it("does not call waitOnTaskRun until .get() is called", () => {
    const wait = createMockWait();
    new TaskRunResult(wait, "run-123");

    expect(wait).not.toHaveBeenCalled();
  });

  it(".get() calls waitOnTaskRun and returns TaskRunDetails", async () => {
    const wait = createMockWait();
    const result = new TaskRunResult(wait, "run-123");

    const details = await result.get();

    expect(wait).toHaveBeenCalledWith("run-123", undefined);
    expect(details).toBe(mockDetails);
  });

  it(".get() caches the promise so that multiple calls share one connection", () => {
    const wait = createMockWait();
    const result = new TaskRunResult(wait, "run-123");

    const promise1 = result.get();
    const promise2 = result.get();

    expect(promise1).toBe(promise2);
    expect(wait).toHaveBeenCalledTimes(1);
  });

  it("forwards abort signal to waitOnTaskRun", async () => {
    const wait = createMockWait();
    const controller = new AbortController();
    const result = new TaskRunResult(wait, "run-123", controller.signal);

    await result.get();

    expect(wait).toHaveBeenCalledWith("run-123", controller.signal);
  });
});
