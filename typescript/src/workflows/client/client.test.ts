import type { Client } from "openapi-fetch";
import { AbortError, ClientError, ServerError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import { WorkflowsClient } from "./client.js";

describe("WorkflowsClient", () => {
  describe("runTask", () => {
    it("throws AbortError if signal already aborted", async () => {
      // No API calls occur; client throws before using the client
      const mockApiClient = {} as unknown as Client<paths>;
      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      const controller = new AbortController();
      controller.abort();
      await expect(client.runTask("task-1", ["data"], controller.signal)).rejects.toBeInstanceOf(
        AbortError,
      );
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
