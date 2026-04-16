import type { Client } from "openapi-fetch";
import { ClientError, ServerError } from "../../errors";
import type { paths } from "../../generated/schema";
import { KeyValueApi } from "./api";

describe("KeyValueApi", () => {
  const getMock = vi.fn().mockRejectedValue(new Error("should not reach API"));
  const postMock = vi.fn().mockRejectedValue(new Error("should not reach API"));
  const mockApiClient = { GET: getMock, POST: postMock } as unknown as Client<paths>;

  const api = new KeyValueApi(mockApiClient);

  const mockGetSuccess = (data: any) => {
    getMock.mockResolvedValueOnce({
      data,
      response: { status: 200 },
    });
  };

  const mockGetError = (status: number, error?: string) => {
    getMock.mockResolvedValueOnce({
      error: error ?? "Error!",
      response: { status },
    });
  };

  const mockPostSuccess = (data: any) => {
    postMock.mockResolvedValueOnce({
      data,
      response: { status: 200 },
    });
  };

  const mockPostError = (status: number, error?: string) => {
    postMock.mockResolvedValueOnce({
      error: error ?? "Error!",
      response: { status },
    });
  };

  describe("findById", () => {
    it("handles API token error", async () => {
      mockGetError(401);

      await expect(api.findById("abc")).rejects.toThrow("API Token is not authorized");
    });

    it("handles unable to find error", async () => {
      mockGetError(404);

      await expect(api.findById("abc")).rejects.toThrow("Unable to locate a Key Value with ID");
    });

    it("handles unknown client error", async () => {
      mockGetError(429, "I'm a teapot!");

      await expect(api.findById("abc")).rejects.toBeInstanceOf(ClientError);
    });

    it("handles unknown server error", async () => {
      mockGetError(500, "Internal server error");

      await expect(api.findById("abc")).rejects.toBeInstanceOf(ServerError);
    });

    it("returns data if no errors", async () => {
      const data = {
        id: "abc",
        status: "available",
      };
      mockGetSuccess(data);

      await expect(api.findById("abc")).resolves.toEqual(data);
    });
  });

  describe("findByName", () => {
    it("handles API token error", async () => {
      mockGetError(401);

      await expect(api.findByName("test-redis", "tea-abc")).rejects.toThrow(
        "API Token is not authorized",
      );
    });

    it("handles unknown client error", async () => {
      mockGetError(429, "I'm a teapot!");

      await expect(api.findByName("test-redis", "tea-abc")).rejects.toBeInstanceOf(ClientError);
    });

    it("handles unknown server error", async () => {
      mockGetError(500, "Internal server error");

      await expect(api.findByName("test-redis", "tea-abc")).rejects.toBeInstanceOf(ServerError);
    });

    it("handles no results", async () => {
      mockGetSuccess([]);

      await expect(api.findByName("test-redis", "tea-abc")).resolves.toBeNull();
    });

    it("returns first entry if no errors", async () => {
      const data = {
        id: "red-abc",
        status: "available",
      };
      mockGetSuccess([
        {
          keyValue: data,
        },
      ]);

      await expect(api.findByName("test-redis", "tea-abc")).resolves.toEqual(data);
    });
  });

  describe("getConnectionInfo", () => {
    it("handles API token error", async () => {
      mockGetError(401);

      await expect(api.getConnectionInfo("red-abc")).rejects.toThrow("API Token is not authorized");
    });

    it("handles unknown client error", async () => {
      mockGetError(429, "I'm a teapot!");

      await expect(api.getConnectionInfo("red-abc")).rejects.toBeInstanceOf(ClientError);
    });

    it("handles unknown server error", async () => {
      mockGetError(500, "Internal server error");

      await expect(api.getConnectionInfo("red-abc")).rejects.toBeInstanceOf(ServerError);
    });

    it("handles Render internal", async () => {
      const internalConnectionString = "redis://red-abc:6239";
      mockGetSuccess({
        internalConnectionString,
        externalConnectionString: "rediss://abc:xyz@red-abc:6239",
      });
      vi.stubEnv("RENDER", "true");

      await expect(api.getConnectionInfo("red-abc")).resolves.toEqual(internalConnectionString);
    });

    it("handles Render external", async () => {
      const externalConnectionString = "rediss://abc:xyz@red-abc:6239";
      mockGetSuccess({
        internalConnectionString: "redis://red-abc:6239",
        externalConnectionString,
      });
      vi.stubEnv("RENDER", undefined);

      await expect(api.getConnectionInfo("red-abc")).resolves.toEqual(externalConnectionString);
    });
  });

  describe("createInstance", () => {
    it("handles API token error", async () => {
      mockPostError(401);

      await expect(
        api.createInstance({ name: "test-redis", plan: "free", ownerId: "tea-abc" }),
      ).rejects.toThrow("API Token is not authorized");
    });
    it("handles unknown client error", async () => {
      mockPostError(429, "I'm a teapot!");

      await expect(
        api.createInstance({ name: "test-redis", plan: "free", ownerId: "tea-abc" }),
      ).rejects.toBeInstanceOf(ClientError);
    });
    it("handles unknown server error", async () => {
      mockPostError(500, "Internal server error");

      await expect(
        api.createInstance({ name: "test-redis", plan: "free", ownerId: "tea-abc" }),
      ).rejects.toBeInstanceOf(ServerError);
    });
    it("returns data if no errors", async () => {
      const data = {
        id: "abc",
        status: "available",
      };
      mockPostSuccess(data);

      await expect(
        api.createInstance({ name: "test-redis", plan: "free", ownerId: "tea-abc" }),
      ).resolves.toEqual(data);
    });
  });
});
