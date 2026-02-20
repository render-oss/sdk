import type { SSEClient } from "./sse.js";
import { TaskRunResult } from "./task-run-result.js";
import type { TaskRunDetails } from "./types.js";

const mockDetails: TaskRunDetails = {
  id: "run-123",
  status: "completed",
  taskId: "task-1",
  results: [42],
} as unknown as TaskRunDetails;

function createMockSSEClient() {
  return {
    waitOnTaskRun: vi.fn().mockResolvedValue(mockDetails),
  } as unknown as SSEClient;
}

describe("TaskRunResult", () => {
  it("does not open SSE connection until .get() is called", () => {
    const sseClient = createMockSSEClient();
    new TaskRunResult(sseClient, "run-123");

    expect(sseClient.waitOnTaskRun).not.toHaveBeenCalled();
  });

  it(".get() calls waitOnTaskRun and returns TaskRunDetails", async () => {
    const sseClient = createMockSSEClient();
    const result = new TaskRunResult(sseClient, "run-123");

    const details = await result.get();

    expect(sseClient.waitOnTaskRun).toHaveBeenCalledWith("run-123", undefined);
    expect(details).toBe(mockDetails);
  });

  it(".get() caches the promise so that multiple calls share one SSE connection", () => {
    const sseClient = createMockSSEClient();
    const result = new TaskRunResult(sseClient, "run-123");

    const promise1 = result.get();
    const promise2 = result.get();

    expect(promise1).toBe(promise2);
    expect(sseClient.waitOnTaskRun).toHaveBeenCalledTimes(1);
  });

  it("forwards abort signal to waitOnTaskRun", async () => {
    const sseClient = createMockSSEClient();
    const controller = new AbortController();
    const result = new TaskRunResult(sseClient, "run-123", controller.signal);

    await result.get();

    expect(sseClient.waitOnTaskRun).toHaveBeenCalledWith("run-123", controller.signal);
  });
});
