import { Readable } from "node:stream";
import type { Client } from "openapi-fetch";
import { ClientError, RenderError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import { ObjectClient } from "./client.js";
import type { PutObjectInput } from "./types.js";

describe("ObjectClient", () => {
  describe("resolveSize (via put validation)", () => {
    // Test resolveSize indirectly by calling put() which will fail
    // at the API call stage, but size validation happens first.
    const putMock = vi.fn().mockRejectedValue(new Error("should not reach API"));
    const mockApiClient = { PUT: putMock } as unknown as Client<paths>;

    const client = new ObjectClient(mockApiClient);

    it("auto-calculates Buffer size", async () => {
      const buffer = Buffer.from("hello");
      putMock.mockResolvedValueOnce({
        data: { url: "http://test", maxSizeBytes: 5 },
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
        "/objects/{ownerId}/{region}/{key}",
        expect.objectContaining({
          body: { sizeBytes: 5 },
        }),
      );
    });

    it("auto-calculates Uint8Array size", async () => {
      const arr = new Uint8Array([1, 2, 3, 4]);
      putMock.mockResolvedValueOnce({
        data: { url: "http://test", maxSizeBytes: 4 },
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
        "/objects/{ownerId}/{region}/{key}",
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
      } as unknown as PutObjectInput;
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

    it("allows zero size for empty files", async () => {
      const stream = Readable.from([]);
      putMock.mockResolvedValueOnce({
        data: { url: "http://test", maxSizeBytes: 0 },
        error: null,
      });

      // Zero-byte uploads should be allowed (will fail at fetch, not validation)
      await expect(
        client.put({
          ownerId: "tea-test",
          region: "oregon",
          key: "test.txt",
          data: stream,
          size: 0,
        }),
      ).rejects.toThrow(); // Will fail at fetch, but size validation passes
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
      ).rejects.toThrow("Size must be a non-negative integer");
    });

    it("throws when file is larger than server maxSizeBytes", async () => {
      const buffer = Buffer.from("hello world"); // 11 bytes
      putMock.mockResolvedValueOnce({
        data: { url: "http://test", maxSizeBytes: 5 }, // Server only allows 5 bytes
        error: null,
      });

      await expect(
        client.put({
          ownerId: "tea-test",
          region: "oregon",
          key: "test.txt",
          data: buffer,
        }),
      ).rejects.toSatisfy((error: Error) => {
        return (
          error instanceof ClientError && error.message.includes("does not match expected size")
        );
      });
    });
  });

  describe("default scope resolution", () => {
    const mockApiClient = {
      PUT: vi.fn(),
      GET: vi.fn(),
      DELETE: vi.fn(),
    } as unknown as Client<paths>;

    it("uses defaults when ownerId/region not provided", () => {
      const client = new ObjectClient(mockApiClient, "tea-default", "oregon");
      // resolveOwnerId/resolveRegion are private, test indirectly via put
      // which will fail at API call but scope resolution happens first
      expect(() => {
        // Access private methods via bracket notation for testing
        const resolveOwnerId = (client as any).resolveOwnerId.bind(client);
        const resolveRegion = (client as any).resolveRegion.bind(client);
        expect(resolveOwnerId(undefined)).toBe("tea-default");
        expect(resolveRegion(undefined)).toBe("oregon");
      }).not.toThrow();
    });

    it("explicit params override defaults", () => {
      const client = new ObjectClient(mockApiClient, "tea-default", "oregon");
      const resolveOwnerId = (client as any).resolveOwnerId.bind(client);
      const resolveRegion = (client as any).resolveRegion.bind(client);
      expect(resolveOwnerId("tea-explicit")).toBe("tea-explicit");
      expect(resolveRegion("frankfurt")).toBe("frankfurt");
    });

    it("throws when neither param nor default provided for ownerId", () => {
      const client = new ObjectClient(mockApiClient);
      const resolveOwnerId = (client as any).resolveOwnerId.bind(client);
      expect(() => resolveOwnerId(undefined)).toThrow(RenderError);
      expect(() => resolveOwnerId(undefined)).toThrow("ownerId is required");
    });

    it("throws when neither param nor default provided for region", () => {
      const client = new ObjectClient(mockApiClient);
      const resolveRegion = (client as any).resolveRegion.bind(client);
      expect(() => resolveRegion(undefined)).toThrow(RenderError);
      expect(() => resolveRegion(undefined)).toThrow("region is required");
    });

    it("partial defaults: only ownerId set", () => {
      const client = new ObjectClient(mockApiClient, "tea-default");
      const resolveOwnerId = (client as any).resolveOwnerId.bind(client);
      const resolveRegion = (client as any).resolveRegion.bind(client);
      expect(resolveOwnerId(undefined)).toBe("tea-default");
      expect(() => resolveRegion(undefined)).toThrow("region is required");
    });

    it("partial defaults: only region set", () => {
      const client = new ObjectClient(mockApiClient, undefined, "oregon");
      const resolveOwnerId = (client as any).resolveOwnerId.bind(client);
      const resolveRegion = (client as any).resolveRegion.bind(client);
      expect(() => resolveOwnerId(undefined)).toThrow("ownerId is required");
      expect(resolveRegion(undefined)).toBe("oregon");
    });
  });

  describe("env var resolution via Render constructor", () => {
    const originalEnv = process.env;

    beforeEach(() => {
      process.env = { ...originalEnv };
    });

    afterAll(() => {
      process.env = originalEnv;
    });

    it("reads RENDER_WORKSPACE_ID and RENDER_REGION from env", async () => {
      process.env.RENDER_API_KEY = "test-token";
      process.env.RENDER_WORKSPACE_ID = "tea-from-env";
      process.env.RENDER_REGION = "frankfurt";

      // Dynamic import to pick up env changes
      const { Render } = await import("../../render.js");
      const render = new Render();

      // Verify defaults propagated through the chain
      const objects = render.experimental.storage.objects;
      const resolveOwnerId = (objects as any).resolveOwnerId.bind(objects);
      const resolveRegion = (objects as any).resolveRegion.bind(objects);
      expect(resolveOwnerId(undefined)).toBe("tea-from-env");
      expect(resolveRegion(undefined)).toBe("frankfurt");
    });

    it("treats empty string env vars as unset", async () => {
      process.env.RENDER_API_KEY = "test-token";
      process.env.RENDER_WORKSPACE_ID = "";
      process.env.RENDER_REGION = "";

      const { Render } = await import("../../render.js");
      const render = new Render();

      const objects = render.experimental.storage.objects;
      const resolveOwnerId = (objects as any).resolveOwnerId.bind(objects);
      const resolveRegion = (objects as any).resolveRegion.bind(objects);
      expect(() => resolveOwnerId(undefined)).toThrow("ownerId is required");
      expect(() => resolveRegion(undefined)).toThrow("region is required");
    });

    it("constructor options override env vars", async () => {
      process.env.RENDER_API_KEY = "test-token";
      process.env.RENDER_WORKSPACE_ID = "tea-from-env";
      process.env.RENDER_REGION = "frankfurt";

      const { Render } = await import("../../render.js");
      const render = new Render({ ownerId: "tea-from-opts", region: "oregon" });

      const objects = render.experimental.storage.objects;
      const resolveOwnerId = (objects as any).resolveOwnerId.bind(objects);
      const resolveRegion = (objects as any).resolveRegion.bind(objects);
      expect(resolveOwnerId(undefined)).toBe("tea-from-opts");
      expect(resolveRegion(undefined)).toBe("oregon");
    });
  });
});
