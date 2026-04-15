import type { Client } from "openapi-fetch";
import { ClientError, ServerError } from "../../errors";
import type { paths } from "../../generated/schema";
import { KeyValueApi } from "./api";

describe("KeyValueApi", () => {
  const getMock = vi.fn().mockRejectedValue(new Error("should not reach API"));
  const mockApiClient = { GET: getMock } as unknown as Client<paths>;

  const api = new KeyValueApi(mockApiClient);

  const mockSuccess = (data: any) => {
    getMock.mockResolvedValueOnce({
      data,
      response: { status: 200 },
    });
  };

  const mockError = (status: number, error?: string) => {
    getMock.mockResolvedValueOnce({
      error: error ?? "Error!",
      response: { status },
    });
  };

  describe("findById", () => {
    it("handles API token error", async () => {
      mockError(401);

      await expect(api.findById("abc")).rejects.toThrow("API Token is not authorized");
    });

    it("handles unable to find error", async () => {
      mockError(404);

      await expect(api.findById("abc")).rejects.toThrow("Unable to locate a Key Value with ID");
    });

    it("handles unknown client error", async () => {
      mockError(429, "I'm a teapot!");

      await expect(api.findById("abc")).rejects.toBeInstanceOf(ClientError);
    });

    it("handles unknown server error", async () => {
      mockError(500, "Internal server error");

      await expect(api.findById("abc")).rejects.toBeInstanceOf(ServerError);
    });

    it("returns data if no errors", async () => {
      const data = {
        id: "abc",
        status: "available",
      };
      mockSuccess(data);

      await expect(api.findById("abc")).resolves.toEqual(data);
    });
  });

  describe("findByName", () => {
    it("handles API token error", async () => {
      mockError(401);

      await expect(api.findByName("test-redis", "tea-abc")).rejects.toThrow(
        "API Token is not authorized",
      );
    });

    it("handles unknown client error", async () => {
      mockError(429, "I'm a teapot!");

      await expect(api.findByName("test-redis", "tea-abc")).rejects.toBeInstanceOf(ClientError);
    });

    it("handles unknown server error", async () => {
      mockError(500, "Internal server error");

      await expect(api.findByName("test-redis", "tea-abc")).rejects.toBeInstanceOf(ServerError);
    });

    it("handles no results", async () => {
      mockSuccess([]);

      await expect(api.findByName("test-redis", "tea-abc")).resolves.toBeNull();
    });

    it("returns first entry if no errors", async () => {
      const data = {
        id: "red-abc",
        status: "available",
      };
      mockSuccess([
        {
          keyValue: data,
        },
      ]);

      await expect(api.findByName("test-redis", "tea-abc")).resolves.toEqual(data);
    });
  });

  describe("getConnectionInfo", () => {
    it("handles API token error", async () => {
      mockError(401);

      await expect(api.getConnectionInfo("red-abc")).rejects.toThrow("API Token is not authorized");
    });

    it("handles unknown client error", async () => {
      mockError(429, "I'm a teapot!");

      await expect(api.getConnectionInfo("red-abc")).rejects.toBeInstanceOf(ClientError);
    });

    it("handles unknown server error", async () => {
      mockError(500, "Internal server error");

      await expect(api.getConnectionInfo("red-abc")).rejects.toBeInstanceOf(ServerError);
    });

    it("handles Render internal", async () => {
      const internalConnectionString = "redis://red-abc:6239";
      mockSuccess({
        internalConnectionString,
        externalConnectionString: "rediss://abc:xyz@red-abc:6239",
      });
      vi.stubEnv("RENDER", "true");

      await expect(api.getConnectionInfo("red-abc")).resolves.toEqual(internalConnectionString);
    });

    it("handles Render external", async () => {
      const externalConnectionString = "rediss://abc:xyz@red-abc:6239";
      mockSuccess({
        internalConnectionString: "redis://red-abc:6239",
        externalConnectionString,
      });
      vi.stubEnv("RENDER", undefined);

      await expect(api.getConnectionInfo("red-abc")).resolves.toEqual(externalConnectionString);
    });
  });
});
