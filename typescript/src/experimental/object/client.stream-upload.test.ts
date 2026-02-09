import { createServer, type IncomingMessage, type Server } from "node:http";
import { Readable } from "node:stream";
import type { Client } from "openapi-fetch";
import type { paths } from "../../generated/schema.js";
import { ObjectClient } from "./client.js";

/**
 * Tests that stream uploads send the correct Content-Length header.
 *
 * Bun's fetch implementation strips the Content-Length header when the body
 * is a stream, even if explicitly set. This causes presigned URL uploads to
 * fail with 403 because the server expects Content-Length to match.
 *
 * See: https://github.com/oven-sh/bun/issues/10507
 */
describe("ObjectClient stream upload Content-Length", () => {
  let server: Server;
  let serverUrl: string;
  let lastReceivedHeaders: IncomingMessage["headers"];
  let lastReceivedBody: Buffer;

  beforeAll(async () => {
    // Start a local HTTP server that captures request headers and body
    server = createServer(async (req, res) => {
      lastReceivedHeaders = req.headers;

      const chunks: Buffer[] = [];
      for await (const chunk of req) {
        chunks.push(Buffer.from(chunk));
      }
      lastReceivedBody = Buffer.concat(chunks);

      res.writeHead(200, { ETag: '"test-etag"' });
      res.end();
    });

    await new Promise<void>((resolve) => {
      server.listen(0, "127.0.0.1", () => resolve());
    });

    const addr = server.address();
    if (typeof addr === "object" && addr !== null) {
      serverUrl = `http://127.0.0.1:${addr.port}`;
    }
  });

  afterAll(async () => {
    await new Promise<void>((resolve) => server.close(() => resolve()));
  });

  beforeEach(() => {
    lastReceivedHeaders = {} as IncomingMessage["headers"];
    lastReceivedBody = Buffer.alloc(0);
  });

  function createMockApiClient(): Client<paths> {
    const putMock = vi.fn().mockResolvedValue({
      data: { url: `${serverUrl}/upload` },
      error: null,
    });
    return { PUT: putMock } as unknown as Client<paths>;
  }

  it("sends Content-Length header when uploading a Readable stream", async () => {
    const content = "hello world - this is stream content for testing";
    const contentSize = Buffer.byteLength(content);
    const stream = Readable.from([content]);

    const client = new ObjectClient(createMockApiClient());
    await client.put({
      ownerId: "tea-test",
      region: "oregon",
      key: "stream-test.txt",
      data: stream,
      size: contentSize,
    });

    // Node's fetch sends this correctly; Bun's fetch strips it for streams.
    // As a workaround, we buffer Readable streams before uploading for Bun compatibility.
    expect(lastReceivedHeaders["content-length"]).toBe(contentSize.toString());
    expect(lastReceivedBody.toString()).toBe(content);
  });

  it("sends Content-Length header when uploading a Buffer", async () => {
    const content = Buffer.from("hello world - buffer content");
    const contentSize = content.byteLength;

    const client = new ObjectClient(createMockApiClient());
    await client.put({
      ownerId: "tea-test",
      region: "oregon",
      key: "buffer-test.txt",
      data: content,
    });

    // Buffer uploads should work in both Node and Bun since the runtime
    // can determine the body size without relying on the explicit header.
    expect(lastReceivedHeaders["content-length"]).toBe(contentSize.toString());
    expect(lastReceivedBody.toString()).toBe(content.toString());
  });

  it("sends correct Content-Length for multi-byte stream content", async () => {
    // Emoji and non-ASCII characters have different byte lengths vs string lengths
    const content = "Hello 🌍 World! Ünïcödë";
    const contentSize = Buffer.byteLength(content);
    const stream = Readable.from([content]);

    const client = new ObjectClient(createMockApiClient());
    await client.put({
      ownerId: "tea-test",
      region: "oregon",
      key: "unicode-test.txt",
      data: stream,
      size: contentSize,
    });

    expect(lastReceivedHeaders["content-length"]).toBe(contentSize.toString());
    expect(lastReceivedBody.toString()).toBe(content);
  });
});
