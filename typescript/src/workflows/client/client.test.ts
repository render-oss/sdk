import type { Client } from "openapi-fetch";
import { AbortError, ClientError, ServerError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import { WorkflowsClient } from "./client.js";
import { TaskEventType } from "./sse.js";
import { TaskRunResult } from "./task-run-result.js";

// ---- EventSource mock (must be hoisted for vi.mock) ----

type ESListener = (event: MessageEvent) => void;

const { MockEventSource } = vi.hoisted(() => {
  class MockEventSource {
    static instances: MockEventSource[] = [];
    url: string;
    listeners = new Map<string, ESListener[]>();
    closed = false;

    constructor(url: string, _opts?: any) {
      this.url = url;
      MockEventSource.instances.push(this);
    }

    addEventListener(type: string, fn: ESListener) {
      const list = this.listeners.get(type) ?? [];
      list.push(fn);
      this.listeners.set(type, list);
    }

    removeEventListener(type: string, fn: ESListener) {
      const list = this.listeners.get(type) ?? [];
      this.listeners.set(
        type,
        list.filter((f) => f !== fn),
      );
    }

    close() {
      this.closed = true;
    }

    // Test helper: emit an event
    emit(type: string, data: any) {
      const listeners = this.listeners.get(type) ?? [];
      const event = { data: JSON.stringify(data) } as MessageEvent;
      for (const fn of listeners) {
        fn(event);
      }
    }

    // Test helper: emit an error
    emitError(message?: string) {
      const listeners = this.listeners.get("error") ?? [];
      const event = { message: message ?? "connection failed" } as any;
      for (const fn of listeners) {
        fn(event);
      }
    }
  }

  return { MockEventSource };
});

vi.mock("eventsource", () => ({
  EventSource: MockEventSource,
}));

function latestEventSource(): InstanceType<typeof MockEventSource> {
  return MockEventSource.instances[MockEventSource.instances.length - 1];
}

beforeEach(() => {
  MockEventSource.instances = [];
});

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

  describe("taskRunEvents", () => {
    it("yields events from SSE stream", async () => {
      const mockApiClient = {} as unknown as Client<paths>;
      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      const gen = client.taskRunEvents(["run-1", "run-2"]);

      // Start iterating — the generator will be waiting for events
      const firstPromise = gen.next();

      const es = latestEventSource();
      expect(es.url).toContain("/v1/task-runs/events");
      expect(es.url).toContain("taskRunIds=run-1%2Crun-2");

      // Emit a completed event
      const completedDetails = { id: "run-1", status: "completed", results: [42] };
      es.emit(TaskEventType.COMPLETED, completedDetails);

      const first = await firstPromise;
      expect(first.value).toEqual(completedDetails);
      expect(first.done).toBe(false);

      // Emit a failed event
      const failedDetails = { id: "run-2", status: "failed", error: "boom" };
      const secondPromise = gen.next();
      es.emit(TaskEventType.FAILED, failedDetails);

      const second = await secondPromise;
      expect(second.value).toEqual(failedDetails);
      expect(second.done).toBe(false);

      // Clean up
      await gen.return(undefined as any);
      expect(es.closed).toBe(true);
    });

    it("throws on SSE connection error", async () => {
      const mockApiClient = {} as unknown as Client<paths>;
      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      const gen = client.taskRunEvents(["run-1"]);
      const promise = gen.next();

      const es = latestEventSource();
      es.emitError("connection refused");

      await expect(promise).rejects.toThrow("SSE connection error: connection refused");
      expect(es.closed).toBe(true);
    });

    it("throws AbortError if signal already aborted", async () => {
      const mockApiClient = {} as unknown as Client<paths>;
      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      const controller = new AbortController();
      controller.abort();

      const gen = client.taskRunEvents(["run-1"], controller.signal);
      await expect(gen.next()).rejects.toBeInstanceOf(AbortError);
    });

    it("throws AbortError when signal is aborted during streaming", async () => {
      const mockApiClient = {} as unknown as Client<paths>;
      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      const controller = new AbortController();
      const gen = client.taskRunEvents(["run-1"], controller.signal);

      const promise = gen.next();

      // Abort the signal
      controller.abort();

      await expect(promise).rejects.toBeInstanceOf(AbortError);

      const es = latestEventSource();
      expect(es.closed).toBe(true);
    });
  });
});
