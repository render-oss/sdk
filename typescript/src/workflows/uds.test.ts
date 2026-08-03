import http from "node:http";
import { UDSClient } from "./uds.js";

vi.mock("node:http");

type RequestCallback = (res: http.IncomingMessage) => void;

const UUID_V4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

// UDSClient request is private, so stub the type for testing.
interface UDSClientRequestable {
  request<T>(path: string, method: string, body?: unknown): Promise<T>;
}

/**
 * Helper to mock http.request with a sequence of responses.
 * Each entry either emits an error or returns an HTTP response.
 */
function mockHttpRequestSequence(
  responses: Array<{ error?: Error; statusCode?: number; body?: string }>,
) {
  let callIndex = 0;
  vi.mocked(http.request).mockImplementation(((
    _options: http.RequestOptions,
    callback?: RequestCallback,
  ) => {
    const response = responses[callIndex] ?? responses[responses.length - 1];
    callIndex++;
    let errorHandler: ((err: Error) => void) | undefined;
    const req = {
      on: vi.fn((event: string, handler: any) => {
        if (event === "error") errorHandler = handler;
      }),
      end: vi.fn(() => {
        setImmediate(() => {
          if (response.error) {
            errorHandler?.(response.error);
          } else {
            const res = {
              statusCode: response.statusCode ?? 200,
              [Symbol.asyncIterator]: async function* () {
                yield Buffer.from(response.body ?? "{}");
              },
            } as unknown as http.IncomingMessage;
            callback?.(res);
          }
        });
      }),
    } as unknown as http.ClientRequest;
    return req;
  }) as typeof http.request);
}

describe("UDSClient", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("request (Content-Length via Buffer.byteLength)", () => {
    it("uses byte length for Content-Length when body contains multi-byte UTF-8", async () => {
      const body = { msg: "😀" }; // emoji: 2 code units (JS .length) vs 4 bytes (UTF-8)
      const bodyString = JSON.stringify(body);
      const byteLength = Buffer.byteLength(bodyString);
      const stringLength = bodyString.length;
      expect(byteLength).toBeGreaterThan(stringLength);

      let capturedOptions: http.RequestOptions | undefined;
      let capturedEndArg: string | undefined;
      vi.mocked(http.request).mockImplementation(((
        options: http.RequestOptions,
        callback?: RequestCallback,
      ) => {
        capturedOptions = options;
        const req = {
          on: vi.fn(),
          end: vi.fn((arg?: string) => {
            capturedEndArg = arg;
          }),
        } as unknown as http.ClientRequest;
        setImmediate(() => {
          const res = {
            statusCode: 200,
            [Symbol.asyncIterator]: async function* () {
              yield Buffer.from("{}");
            },
          } as unknown as http.IncomingMessage;
          callback?.(res);
        });
        return req;
      }) as typeof http.request);

      const client = new UDSClient("/tmp/test.sock") as unknown as UDSClientRequestable;
      await client.request("/test", "POST", body);

      const headers = capturedOptions?.headers as Record<string, number> | undefined;
      expect(headers?.["Content-Length"]).toBe(byteLength);
      expect(headers?.["Content-Length"]).not.toBe(stringLength);
      expect(capturedEndArg).toBe(bodyString);
    });

    it("uses Content-Length 0 for GET requests with no body", async () => {
      let capturedOptions: http.RequestOptions | undefined;
      vi.mocked(http.request).mockImplementation(((
        options: http.RequestOptions,
        callback?: RequestCallback,
      ) => {
        capturedOptions = options;
        const req = {
          on: vi.fn(),
          end: vi.fn(),
        } as unknown as http.ClientRequest;
        setImmediate(() => {
          const res = {
            statusCode: 200,
            [Symbol.asyncIterator]: async function* () {
              yield Buffer.from("{}");
            },
          } as unknown as http.IncomingMessage;
          callback?.(res);
        });
        return req;
      }) as typeof http.request);

      const client = new UDSClient("/tmp/test.sock") as unknown as UDSClientRequestable;
      await client.request("/input", "GET");

      const headers = capturedOptions?.headers as Record<string, number> | undefined;
      expect(headers?.["Content-Length"]).toBe(0);
    });
  });

  describe("runSubtask", () => {
    /** Mocks http.request to always succeed, collecting each request body. */
    function mockHttpRequestCapturingBodies(): string[] {
      const capturedBodies: string[] = [];
      vi.mocked(http.request).mockImplementation(((
        _options: http.RequestOptions,
        callback?: RequestCallback,
      ) => {
        const req = {
          on: vi.fn(),
          end: vi.fn((arg?: string) => {
            if (arg !== undefined) capturedBodies.push(arg);
          }),
        } as unknown as http.ClientRequest;
        setImmediate(() => {
          const res = {
            statusCode: 200,
            [Symbol.asyncIterator]: async function* () {
              yield Buffer.from('{"task_run_id":"trn-1"}');
            },
          } as unknown as http.IncomingMessage;
          callback?.(res);
        });
        return req;
      }) as typeof http.request);
      return capturedBodies;
    }

    it("sets idempotency_key and created_at on the request body", async () => {
      const capturedBodies = mockHttpRequestCapturingBodies();

      const client = new UDSClient("/tmp/test.sock");
      const taskRunId = await client.runSubtask("my-task", ["arg"]);
      expect(taskRunId).toBe("trn-1");

      const body = JSON.parse(capturedBodies[0] ?? "{}");
      expect(body.idempotency_key).toMatch(UUID_V4);
      expect(typeof body.created_at).toBe("string");
      // created_at must be a valid timestamp.
      expect(Number.isNaN(Date.parse(body.created_at))).toBe(false);
    });

    it("generates a distinct idempotency_key per call", async () => {
      const capturedBodies = mockHttpRequestCapturingBodies();

      const client = new UDSClient("/tmp/test.sock");
      await client.runSubtask("my-task", ["arg"]);
      await client.runSubtask("my-task", ["arg"]);

      const keys = capturedBodies.map((body) => JSON.parse(body).idempotency_key);
      expect(keys).toHaveLength(2);
      expect(keys[0]).toMatch(UUID_V4);
      expect(keys[1]).toMatch(UUID_V4);
      expect(keys[0]).not.toBe(keys[1]);
    });
  });

  describe("retry on transient errors", () => {
    beforeEach(() => {
      vi.useFakeTimers();
    });

    afterEach(() => {
      vi.useRealTimers();
    });

    it("retries on connection error then succeeds", async () => {
      mockHttpRequestSequence([
        { error: new Error("connect ECONNREFUSED /render/render.sock") },
        { error: new Error("connect ENOENT /render/render.sock") },
        { statusCode: 200, body: '{"task_name":"test","input":"W10="}' },
      ]);

      const client = new UDSClient("/tmp/test.sock");
      const promise = client.getInput();
      await vi.runAllTimersAsync();
      const result = await promise;

      expect(result.task_name).toBe("test");
      expect(http.request).toHaveBeenCalledTimes(3);
    });

    it("retries on 5xx then succeeds", async () => {
      mockHttpRequestSequence([
        { statusCode: 500, body: "internal server error" },
        { statusCode: 200, body: "{}" },
      ]);

      const client = new UDSClient("/tmp/test.sock");
      const promise = client.sendCallback("result");
      await vi.runAllTimersAsync();
      await promise;

      expect(http.request).toHaveBeenCalledTimes(2);
    });

    it("retries on 429 then succeeds", async () => {
      mockHttpRequestSequence([
        { statusCode: 429, body: "rate limited" },
        { statusCode: 200, body: "{}" },
      ]);

      const client = new UDSClient("/tmp/test.sock");
      const promise = client.sendCallback("result");
      await vi.runAllTimersAsync();
      await promise;

      expect(http.request).toHaveBeenCalledTimes(2);
    });

    it("does not retry on 4xx client error", async () => {
      mockHttpRequestSequence([{ statusCode: 400, body: "bad request" }]);

      const client = new UDSClient("/tmp/test.sock");
      const promise = client.sendCallback("result");
      // Attach rejection handler before advancing timers to avoid unhandled rejection warnings
      const assertion = expect(promise).rejects.toThrow("HTTP 400: bad request");
      await vi.runAllTimersAsync();

      await assertion;
      expect(http.request).toHaveBeenCalledTimes(1);
    });

    it("throws after exhausting all retries", async () => {
      mockHttpRequestSequence([{ error: new Error("connect ECONNREFUSED /render/render.sock") }]);

      const client = new UDSClient("/tmp/test.sock");
      const promise = client.sendCallback("result");
      const assertion = expect(promise).rejects.toThrow("ECONNREFUSED");
      await vi.runAllTimersAsync();

      await assertion;
      expect(http.request).toHaveBeenCalledTimes(25);
    });
  });
});
