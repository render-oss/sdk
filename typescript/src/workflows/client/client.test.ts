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
    emitError(message?: string, status?: number) {
      const listeners = this.listeners.get("error") ?? [];
      const event = { message: message ?? "connection failed" } as any;
      event.code = status;
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

// ---- Flow run helpers ----

type FakeApi = {
  POST: ReturnType<typeof vi.fn>;
  GET: ReturnType<typeof vi.fn>;
  DELETE: ReturnType<typeof vi.fn>;
};

function flowRunDetails(status: string) {
  return { id: "frn-1", flowId: "flw-1", status, input: [], results: [], attempts: [] };
}

function ok(data?: unknown) {
  return { data, error: undefined, response: { status: 200 } };
}

function apiError(status: number) {
  return { data: undefined, error: { message: "nope", id: "err-1" }, response: { status } };
}

// Builds a client whose API calls all succeed; each test overrides only the calls it cares about.
function newFlowClient(overrides: Partial<FakeApi> = {}) {
  const api: FakeApi = {
    POST: vi.fn().mockResolvedValue(ok({ id: "frn-1", flowId: "flw-1", status: "pending" })),
    GET: vi.fn().mockResolvedValue(ok(flowRunDetails("succeeded"))),
    DELETE: vi.fn().mockResolvedValue(ok()),
    ...overrides,
  };
  const client = new WorkflowsClient(api as unknown as Client<paths>, "http://test", "token");
  return { api, client };
}

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

    it("omits idempotencyKey from the body when none is given", async () => {
      const mockApiClient = {
        POST: vi.fn().mockResolvedValue({
          data: { id: "run-456" },
          error: undefined,
          response: { status: 200 },
        }),
      } as unknown as Client<paths>;

      const client = new WorkflowsClient(mockApiClient, "http://test", "token");
      await client.startTask("workflow/task", [1, 2]);

      expect(mockApiClient.POST).toHaveBeenCalledWith("/task-runs", {
        body: { task: "workflow/task", input: [1, 2] },
        signal: undefined,
      });
    });

    it("sends the idempotencyKey from the options object", async () => {
      const mockApiClient = {
        POST: vi.fn().mockResolvedValue({
          data: { id: "run-456" },
          error: undefined,
          response: { status: 200 },
        }),
      } as unknown as Client<paths>;

      const controller = new AbortController();
      const client = new WorkflowsClient(mockApiClient, "http://test", "token");
      await client.startTask("workflow/task", [1, 2], {
        idempotencyKey: "order-42",
        signal: controller.signal,
      });

      expect(mockApiClient.POST).toHaveBeenCalledWith("/task-runs", {
        body: { task: "workflow/task", input: [1, 2], idempotencyKey: "order-42" },
        signal: controller.signal,
      });
    });

    it("throws AbortError if the options object carries an aborted signal", async () => {
      const mockApiClient = {} as unknown as Client<paths>;
      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      const controller = new AbortController();
      controller.abort();
      await expect(
        client.startTask("task-1", ["data"], { signal: controller.signal }),
      ).rejects.toBeInstanceOf(AbortError);
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

    it("passes the idempotencyKey through to the request body", async () => {
      const mockApiClient = {
        POST: vi.fn().mockResolvedValue({
          data: { id: "run-456" },
          error: undefined,
          response: { status: 200 },
        }),
      } as unknown as Client<paths>;

      const getSpy = vi.spyOn(TaskRunResult.prototype, "get").mockResolvedValue({} as any);

      const client = new WorkflowsClient(mockApiClient, "http://test", "token");
      await client.runTask("workflow/task", [4], { idempotencyKey: "order-42" });

      expect(mockApiClient.POST).toHaveBeenCalledWith("/task-runs", {
        body: { task: "workflow/task", input: [4], idempotencyKey: "order-42" },
        signal: undefined,
      });
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
      await expect(client.listTaskRuns({ taskSlug: ["task-1"] })).rejects.toBeInstanceOf(
        ClientError,
      );
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
      const completedDetails = {
        id: "run-1",
        status: "completed",
        results: [42],
      };
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

      // Emit a canceled event
      const canceledDetails = { id: "run-3", status: "canceled" };
      const thirdPromise = gen.next();
      es.emit(TaskEventType.CANCELED, canceledDetails);

      const third = await thirdPromise;
      expect(third.value).toEqual(canceledDetails);
      expect(third.done).toBe(false);

      // Clean up
      await gen.return(undefined as any);
      expect(es.closed).toBe(true);
    });

    it("throws on SSE connection error after 5 retries with backoff", async () => {
      vi.useFakeTimers();
      const mockApiClient = {} as unknown as Client<paths>;
      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      const gen = client.taskRunEvents(["run-1"]);
      const promise = gen.next();

      // Attempt 0
      let es = latestEventSource();
      es.emitError("connection refused");

      // Wait 250ms (first backoff)
      await vi.advanceTimersByTimeAsync(250);

      // Attempt 1
      es = latestEventSource();
      es.emitError("connection refused");

      // Wait 500ms
      await vi.advanceTimersByTimeAsync(500);

      // Attempt 2
      es = latestEventSource();
      es.emitError("connection refused");

      // Wait 1000ms
      await vi.advanceTimersByTimeAsync(1000);

      // Attempt 3
      es = latestEventSource();
      es.emitError("connection refused");

      // Wait 2000ms
      await vi.advanceTimersByTimeAsync(2000);

      // Attempt 4
      es = latestEventSource();
      es.emitError("connection refused");

      // Wait 4000ms
      await vi.advanceTimersByTimeAsync(4000);

      // Attempt 5 (6th connection error) - should propagate
      es = latestEventSource();
      es.emitError("connection refused");

      await expect(promise).rejects.toThrow("SSE connection error: connection refused");
      expect(es.closed).toBe(true);

      vi.useRealTimers();
    });

    it("throws immediately on non-connection related error", async () => {
      const mockApiClient = {} as unknown as Client<paths>;
      const client = new WorkflowsClient(mockApiClient, "http://test", "token");

      const gen = client.taskRunEvents(["run-1"]);
      const promise = gen.next();

      const es = latestEventSource();
      es.emitError("Forbidden", 403);

      await expect(promise).rejects.toThrow("SSE connection error: Forbidden");
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
  describe("startFlow", () => {
    it("returns the started flow run", async () => {
      const { client } = newFlowClient();

      const flowRun = await client.startFlow("workflow/flow", [1, 2]);

      expect(flowRun).toEqual({ id: "frn-1", flowId: "flw-1", status: "pending" });
    });

    it.each([
      {
        name: "no options",
        options: undefined,
        body: { flow: "workflow/flow", input: { a: 1 } },
        signal: undefined,
      },
      {
        name: "an idempotency key",
        options: { idempotencyKey: "order-42" },
        body: { flow: "workflow/flow", input: { a: 1 }, idempotencyKey: "order-42" },
        signal: undefined,
      },
    ])("sends the request body with $name", async ({ options, body, signal }) => {
      const { api, client } = newFlowClient();

      await client.startFlow("workflow/flow", { a: 1 }, options);

      expect(api.POST).toHaveBeenCalledWith("/flow-runs", { body, signal });
    });

    it.each([
      { name: "a bare signal", wrap: (signal: AbortSignal) => signal },
      { name: "an options object", wrap: (signal: AbortSignal) => ({ signal }) },
    ])("forwards $name to the request", async ({ wrap }) => {
      const { api, client } = newFlowClient();
      const controller = new AbortController();

      await client.startFlow("workflow/flow", [], wrap(controller.signal));

      expect(api.POST).toHaveBeenCalledWith("/flow-runs", {
        body: { flow: "workflow/flow", input: [] },
        signal: controller.signal,
      });
    });

    it.each([
      { name: "a bare signal", wrap: (signal: AbortSignal) => signal },
      { name: "an options object", wrap: (signal: AbortSignal) => ({ signal }) },
    ])("throws AbortError without a request if $name is already aborted", async ({ wrap }) => {
      const { api, client } = newFlowClient();
      const controller = new AbortController();
      controller.abort();

      await expect(
        client.startFlow("workflow/flow", [], wrap(controller.signal)),
      ).rejects.toBeInstanceOf(AbortError);
      expect(api.POST).not.toHaveBeenCalled();
    });

    it("converts a DOM AbortError from the request into AbortError", async () => {
      const { client } = newFlowClient({
        POST: vi.fn().mockRejectedValue(new DOMException("aborted", "AbortError")),
      });

      await expect(client.startFlow("workflow/flow", [])).rejects.toBeInstanceOf(AbortError);
    });
  });

  describe("runFlow", () => {
    beforeEach(() => {
      vi.useFakeTimers();
    });

    afterEach(() => {
      vi.useRealTimers();
    });

    function getFlowRunReturning(...statuses: string[]) {
      const GET = vi.fn();
      for (const status of statuses) GET.mockResolvedValueOnce(ok(flowRunDetails(status)));
      return GET;
    }

    it.each([
      { name: "succeeds", statuses: ["pending", "running", "paused", "succeeded"] },
      { name: "fails", statuses: ["running", "failed"] },
      { name: "is canceled", statuses: ["canceled"] },
    ])("polls until the flow run $name and resolves with its details", async ({ statuses }) => {
      const { api, client } = newFlowClient({ GET: getFlowRunReturning(...statuses) });

      const result = client.runFlow("workflow/flow", [1]);
      await vi.advanceTimersByTimeAsync(60_000);

      await expect(result).resolves.toEqual(flowRunDetails(statuses[statuses.length - 1]));
      expect(api.GET).toHaveBeenCalledTimes(statuses.length);
      expect(api.GET).toHaveBeenCalledWith("/flow-runs/{flowRunId}", {
        params: { path: { flowRunId: "frn-1" } },
        signal: expect.any(AbortSignal),
      });
    });

    it("passes the idempotencyKey through to the request body", async () => {
      const { api, client } = newFlowClient();

      await client.runFlow("workflow/flow", [1], { idempotencyKey: "order-42" });

      expect(api.POST).toHaveBeenCalledWith("/flow-runs", {
        body: { flow: "workflow/flow", input: [1], idempotencyKey: "order-42" },
        signal: undefined,
      });
    });

    it.each([
      { name: "a bare signal", wrap: (signal: AbortSignal) => signal },
      { name: "an options object", wrap: (signal: AbortSignal) => ({ signal }) },
    ])("rejects with AbortError when $name aborts while waiting", async ({ wrap }) => {
      const { api, client } = newFlowClient({
        GET: vi.fn().mockResolvedValue(ok(flowRunDetails("running"))),
      });
      const controller = new AbortController();

      const result = client.runFlow("workflow/flow", [1], wrap(controller.signal));
      const rejected = expect(result).rejects.toBeInstanceOf(AbortError);
      await vi.advanceTimersByTimeAsync(1500);
      controller.abort();
      await vi.advanceTimersByTimeAsync(60_000);

      await rejected;
      expect(api.GET).toHaveBeenCalledTimes(2);
    });

    it("throws the start error without polling", async () => {
      const { api, client } = newFlowClient({ POST: vi.fn().mockResolvedValue(apiError(404)) });

      await expect(client.runFlow("workflow/flow", [1])).rejects.toBeInstanceOf(ClientError);
      expect(api.GET).not.toHaveBeenCalled();
    });
  });

  describe("getFlowRun", () => {
    it("returns the flow run details", async () => {
      const { api, client } = newFlowClient();

      const details = await client.getFlowRun("frn-1");

      expect(details).toEqual(flowRunDetails("succeeded"));
      expect(api.GET).toHaveBeenCalledWith("/flow-runs/{flowRunId}", {
        params: { path: { flowRunId: "frn-1" } },
      });
    });
  });

  describe("cancelFlowRun", () => {
    it("calls DELETE on the flow run endpoint", async () => {
      const { api, client } = newFlowClient();

      await client.cancelFlowRun("frn-1");

      expect(api.DELETE).toHaveBeenCalledWith("/flow-runs/{flowRunId}", {
        params: { path: { flowRunId: "frn-1" } },
      });
    });
  });

  describe("listFlowRuns", () => {
    it("passes the filters as query params and returns the runs", async () => {
      const runs = [{ flowRun: flowRunDetails("running"), cursor: "c-1" }];
      const { api, client } = newFlowClient({ GET: vi.fn().mockResolvedValue(ok(runs)) });
      const params = { flowSlug: ["workflow/flow"], status: ["running" as const], limit: 10 };

      const result = await client.listFlowRuns(params);

      expect(result).toBe(runs);
      expect(api.GET).toHaveBeenCalledWith("/flow-runs", { params: { query: params } });
    });

    it("lists all flow runs when called without filters", async () => {
      const { api, client } = newFlowClient({ GET: vi.fn().mockResolvedValue(ok([])) });

      await client.listFlowRuns();

      expect(api.GET).toHaveBeenCalledWith("/flow-runs", { params: { query: {} } });
    });
  });

  describe("flow run requests with a signal", () => {
    type Call = (client: WorkflowsClient, signal: AbortSignal) => Promise<unknown>;
    const calls: { name: string; method: "GET" | "DELETE"; path: string; call: Call }[] = [
      {
        name: "getFlowRun",
        method: "GET",
        path: "/flow-runs/{flowRunId}",
        call: (c, signal) => c.getFlowRun("frn-1", signal),
      },
      {
        name: "cancelFlowRun",
        method: "DELETE",
        path: "/flow-runs/{flowRunId}",
        call: (c, signal) => c.cancelFlowRun("frn-1", signal),
      },
      {
        name: "listFlowRuns",
        method: "GET",
        path: "/flow-runs",
        call: (c, signal) => c.listFlowRuns({}, signal),
      },
    ];

    it.each(calls)("$name forwards the signal to the request", async ({ method, path, call }) => {
      const { api, client } = newFlowClient({ GET: vi.fn().mockResolvedValue(ok([])) });
      const controller = new AbortController();

      await call(client, controller.signal);

      expect(api[method]).toHaveBeenCalledWith(
        path,
        expect.objectContaining({ signal: controller.signal }),
      );
    });

    it.each(calls)(
      "$name throws AbortError without a request if the signal is already aborted",
      async ({ method, call }) => {
        const { api, client } = newFlowClient();
        const controller = new AbortController();
        controller.abort();

        await expect(call(client, controller.signal)).rejects.toBeInstanceOf(AbortError);
        expect(api[method]).not.toHaveBeenCalled();
      },
    );

    it.each(calls)(
      "$name converts a DOM AbortError from the request into AbortError",
      async ({ method, call }) => {
        const { client } = newFlowClient({
          [method]: vi.fn().mockRejectedValue(new DOMException("aborted", "AbortError")),
        });

        await expect(call(client, new AbortController().signal)).rejects.toBeInstanceOf(AbortError);
      },
    );
  });

  describe("flow run API errors", () => {
    type Call = (client: WorkflowsClient) => Promise<unknown>;
    const calls: { name: string; method: keyof FakeApi; call: Call; message: string }[] = [
      {
        name: "startFlow",
        method: "POST",
        call: (c) => c.startFlow("workflow/flow", []),
        message: "Failed to start flow run",
      },
      {
        name: "getFlowRun",
        method: "GET",
        call: (c) => c.getFlowRun("frn-1"),
        message: "Failed to get flow run",
      },
      {
        name: "cancelFlowRun",
        method: "DELETE",
        call: (c) => c.cancelFlowRun("frn-1"),
        message: "Failed to cancel flow run",
      },
      {
        name: "listFlowRuns",
        method: "GET",
        call: (c) => c.listFlowRuns(),
        message: "Failed to list flow runs",
      },
    ];
    const cases = calls.flatMap((c) => [
      { ...c, status: 404, errorType: ClientError },
      { ...c, status: 500, errorType: ServerError },
    ]);

    it.each(cases)(
      "$name throws $errorType.name for a $status response",
      async ({ method, call, message, status, errorType }) => {
        const { client } = newFlowClient({ [method]: vi.fn().mockResolvedValue(apiError(status)) });

        const err = (await call(client).catch((e) => e)) as Error;

        expect(err).toBeInstanceOf(errorType);
        expect(err).toMatchObject({ statusCode: status });
        expect(err.message).toContain(message);
      },
    );
  });
});
