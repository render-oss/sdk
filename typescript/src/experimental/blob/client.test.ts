import { Readable } from "node:stream";
import type { Client } from "openapi-fetch";
import { RenderError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import { BlobClient } from "./client.js";
import type { PutBlobInput } from "./types.js";

describe("BlobClient", () => {
  describe("resolveSize (via put validation)", () => {
    // Test resolveSize indirectly by calling put() which will fail
    // at the API call stage, but size validation happens first.
    const putMock = vi.fn().mockRejectedValue(new Error("should not reach API"));
    const mockApiClient = { PUT: putMock } as unknown as Client<paths>;

    const client = new BlobClient(mockApiClient);

    it("auto-calculates Buffer size", async () => {
      const buffer = Buffer.from("hello");
      putMock.mockResolvedValueOnce({
        data: { url: "http://test" },
        error: null,
      });

      // Will fail at fetch, but that's after size validation
      await expect(
        client.put({
          ownerId: "tea-test",
          region: "oregon",
          key: "test.txt",
          data: buffer,
        }),
      ).rejects.toThrow(); // fetch not available in test

      expect(putMock).toHaveBeenCalledWith(
        "/blobs/{ownerId}/{region}/{key}",
        expect.objectContaining({
          body: { sizeBytes: 5 },
        }),
      );
    });

    it("auto-calculates Uint8Array size", async () => {
      const arr = new Uint8Array([1, 2, 3, 4]);
      putMock.mockResolvedValueOnce({
        data: { url: "http://test" },
        error: null,
      });

      await expect(
        client.put({
          ownerId: "tea-test",
          region: "oregon",
          key: "test.bin",
          data: arr,
        }),
      ).rejects.toThrow();

      expect(putMock).toHaveBeenCalledWith(
        "/blobs/{ownerId}/{region}/{key}",
        expect.objectContaining({
          body: { sizeBytes: 4 },
        }),
      );
    });

    it("throws on size mismatch for Buffer", async () => {
      const buffer = Buffer.from("hello");
      await expect(
        client.put({
          ownerId: "tea-test",
          region: "oregon",
          key: "test.txt",
          data: buffer,
          size: 10,
        }),
      ).rejects.toThrow(RenderError);
      await expect(
        client.put({
          ownerId: "tea-test",
          region: "oregon",
          key: "test.txt",
          data: buffer,
          size: 10,
        }),
      ).rejects.toThrow("Size mismatch");
    });

    it("requires size for stream input", async () => {
      const stream = Readable.from(["hello"]);
      const invalidInput = {
        ownerId: "tea-test",
        region: "oregon",
        key: "test.txt",
        data: stream,
        // Intentionally omit size to test validation (invalid at runtime)
      } as unknown as PutBlobInput;
      await expect(client.put(invalidInput)).rejects.toThrow(RenderError);
      await expect(client.put(invalidInput)).rejects.toThrow("Size is required");
    });

    it("requires size for string input", async () => {
      await expect(
        client.put({
          ownerId: "tea-test",
          region: "oregon",
          key: "test.txt",
          data: "hello",
        }),
      ).rejects.toThrow("Size is required");
    });

    it("throws on zero size", async () => {
      const stream = Readable.from(["hello"]);
      await expect(
        client.put({
          ownerId: "tea-test",
          region: "oregon",
          key: "test.txt",
          data: stream,
          size: 0,
        }),
      ).rejects.toThrow("Size must be a positive integer");
    });

    it("throws on negative size", async () => {
      const stream = Readable.from(["hello"]);
      await expect(
        client.put({
          ownerId: "tea-test",
          region: "oregon",
          key: "test.txt",
          data: stream,
          size: -1,
        }),
      ).rejects.toThrow("Size must be a positive integer");
    });
  });
});
