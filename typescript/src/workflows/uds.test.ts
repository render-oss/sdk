import http from "node:http";
import { UDSClient } from "./uds.js";

vi.mock("node:http");

type RequestCallback = (res: http.IncomingMessage) => void;

// UDSClient request is private, so stub the type for testing.
interface UDSClientRequestable {
  request<T>(path: string, method: string, body?: unknown): Promise<T>;
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
});
