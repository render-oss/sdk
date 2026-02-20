import type { Client } from "openapi-fetch";
import { AbortError, ClientError, ServerError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import { WorkflowsClient } from "./client.js";
import { TaskRunResult } from "./task-run-result.js";

describe("WorkflowsClient", () => {
  describe("startTask", () => {
    it("throws AbortError if signal already aborted", async () => {
      const mockApiClient = {} as unknown as Client<paths>;
      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      const controller = new AbortController();
      controller.abort();
      await expect(client.startTask("task-1", ["data"], controller.signal)).rejects.toBeInstanceOf(
        AbortError,
      );
    });

    it("returns a TaskRunResult with the correct taskRunId", async () => {
      const mockApiClient = {
        POST: vi.fn().mockResolvedValue({
          data: { id: "run-456" },
          error: undefined,
          response: { status: 200 },
        }),
      } as unknown as Client<paths>;

      const client = new WorkflowsClient(mockApiClient, "http://test", "token");
      const result = await client.startTask("workflow/task", [1, 2]);

      expect(result).toBeInstanceOf(TaskRunResult);
      expect(result.taskRunId).toBe("run-456");
    });
  });

  describe("runTask", () => {
    it("starts the task and returns the awaited result", async () => {
      const mockDetails = {
        id: "run-456",
        status: "completed",
        results: [16],
      };

      const mockApiClient = {
        POST: vi.fn().mockResolvedValue({
          data: { id: "run-456" },
          error: undefined,
          response: { status: 200 },
        }),
      } as unknown as Client<paths>;

      // Patch TaskRunResult.prototype.get to return mock details
      const getSpy = vi.spyOn(TaskRunResult.prototype, "get").mockResolvedValue(mockDetails as any);

      const client = new WorkflowsClient(mockApiClient, "http://test", "token");
      const details = await client.runTask("workflow/task", [4]);

      expect(details).toBe(mockDetails);
      getSpy.mockRestore();
    });
  });

  describe("cancelTaskRun", () => {
    it("calls DELETE on the task run endpoint", async () => {
      const mockApiClient = {
        DELETE: vi.fn().mockResolvedValue({
          error: undefined,
          response: { status: 200 },
        }),
      } as unknown as Client<paths>;

      const client = new WorkflowsClient(mockApiClient, "http://test", "token");
      await client.cancelTaskRun("run-123");

      expect(mockApiClient.DELETE).toHaveBeenCalledWith("/task-runs/{taskRunId}", {
        params: { path: { taskRunId: "run-123" } },
      });
    });
  });

  describe("handleApiError (via getTaskRun)", () => {
    it("throws ServerError for 5xx status", async () => {
      const mockApiClient = {
        GET: vi.fn().mockResolvedValue({
          error: { message: "Internal error" },
          response: { status: 500 },
        }),
      } as unknown as Client<paths>;

      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      await expect(client.getTaskRun("run-123")).rejects.toBeInstanceOf(ServerError);
      await expect(client.getTaskRun("run-123")).rejects.toMatchObject({
        statusCode: 500,
      });
    });

    it("throws ClientError for 4xx status", async () => {
      const mockApiClient = {
        GET: vi.fn().mockResolvedValue({
          error: { message: "Not found" },
          response: { status: 404 },
        }),
      } as unknown as Client<paths>;

      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      await expect(client.getTaskRun("run-123")).rejects.toBeInstanceOf(ClientError);
      await expect(client.getTaskRun("run-123")).rejects.toMatchObject({
        statusCode: 404,
      });
    });
  });

  describe("listTaskRuns", () => {
    it("throws ClientError for 400 status", async () => {
      const mockApiClient = {
        GET: vi.fn().mockResolvedValue({
          error: { message: "Bad request" },
          response: { status: 400 },
        }),
      } as unknown as Client<paths>;

      const client = new WorkflowsClient(mockApiClient, "http://test", "token");
      await expect(client.listTaskRuns({ taskId: ["task-1"] })).rejects.toBeInstanceOf(ClientError);
    });
  });
});
