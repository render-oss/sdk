import type { KeyValueApi } from "./api";
import { KeyValueProvider } from "./provider";

describe("KeyValueProvider", () => {
  const findByIdMock = vi.fn().mockRejectedValue(new Error("should not be called"));
  const findByNameMock = vi.fn().mockRejectedValue(new Error("should not be called"));
  const getConnectionInfoMock = vi.fn().mockRejectedValue(new Error("should not be called"));
  const api = {
    findById: findByIdMock,
    findByName: findByNameMock,
    getConnectionInfo: getConnectionInfoMock,
  } as unknown as KeyValueApi;

  describe("with defaultOwnerId", () => {
    const provider = new KeyValueProvider(api, "tea-abc");

    describe("newClient with name option", () => {
      it("creates client", async () => {
        findByNameMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockResolvedValueOnce("redis://localhosta:6239");

        await expect(provider.newClient({ name: "test-redis" })).resolves.toBeDefined();

        expect(getConnectionInfoMock).toHaveBeenCalledWith("red-abc");
      });
    });

    describe("connectionInfo with name option", () => {
      it("parses connection info", async () => {
        findByNameMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockResolvedValueOnce("redis://localhosta:6239");

        await expect(provider.connectionInfo({ name: "test-redis" })).resolves.toEqual({
          host: "localhosta",
          port: 6239,
        });

        expect(getConnectionInfoMock).toHaveBeenCalledWith("red-abc");
      });
    });
  });

  describe("without defaultOwnerId", () => {
    const client = new KeyValueProvider(api);

    describe("newClient with service ID option", () => {
      it("creates client", async () => {
        findByIdMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockResolvedValueOnce("redis://localhosta:6239");

        await expect(client.newClient({ serviceId: "red-abc" })).resolves.toBeDefined();

        expect(getConnectionInfoMock).toHaveBeenCalledWith("red-abc");
      });
      it("errors if service ID not found", async () => {
        const error = new Error("Unable to find ID");
        findByIdMock.mockRejectedValueOnce(error);

        await expect(client.newClient({ serviceId: "red-abc" })).rejects.toEqual(error);
      });
      it("errors if connection info not found", async () => {
        const error = new Error("Unable to find connection info");
        findByIdMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockRejectedValueOnce(error);

        await expect(client.newClient({ serviceId: "red-abc" })).rejects.toEqual(error);
      });
    });

    describe("newClient with name option", () => {
      it("creates client", async () => {
        findByNameMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockResolvedValueOnce("redis://localhosta:6239");

        await expect(
          client.newClient({ name: "test-redis", ownerId: "tea-abc" }),
        ).resolves.toBeDefined();

        expect(getConnectionInfoMock).toHaveBeenCalledWith("red-abc");
      });
      it("errors if owner id is missing", async () => {
        await expect(client.newClient({ name: "test-redis" })).rejects.toThrow(
          "ownerId is required",
        );
      });
      it("errors if no data returned", async () => {
        findByNameMock.mockResolvedValueOnce(null);

        await expect(client.newClient({ name: "test-redis", ownerId: "tea-abc" })).rejects.toThrow(
          "Unable to locate Key Value",
        );
      });
      it("errors if connection info not found", async () => {
        const error = new Error("Unable to find connection info");
        findByNameMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockRejectedValueOnce(error);

        await expect(client.newClient({ name: "test-redis", ownerId: "tea-abc" })).rejects.toEqual(
          error,
        );
      });
    });

    describe("connectionInfo with service ID option", () => {
      it("parses connection info", async () => {
        findByIdMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockResolvedValueOnce("redis://localhosta:6239");

        await expect(client.connectionInfo({ serviceId: "red-abc" })).resolves.toEqual({
          host: "localhosta",
          port: 6239,
        });
      });
      it("parses connection info with username and password", async () => {
        findByIdMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockResolvedValueOnce("redis://user:pass@localhosta:6239");

        await expect(client.connectionInfo({ serviceId: "red-abc" })).resolves.toEqual({
          host: "localhosta",
          port: 6239,
          username: "user",
          password: "pass",
        });
      });
      it("errors if connection info is invalid format", async () => {
        findByIdMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockResolvedValueOnce("redis://noport.com");

        await expect(client.connectionInfo({ serviceId: "red-abc" })).rejects.toThrow(
          "an unexpected format",
        );
      });
      it("errors if service ID not found", async () => {
        const error = new Error("Unable to find service ID");
        findByIdMock.mockRejectedValueOnce(error);

        await expect(client.connectionInfo({ serviceId: "red-abc" })).rejects.toEqual(error);
      });
      it("errors if connection info not found", async () => {
        const error = new Error("Unable to find connection info");
        findByIdMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockRejectedValueOnce(error);

        await expect(client.connectionInfo({ serviceId: "red-abc" })).rejects.toEqual(error);
      });
    });

    describe("connectionInfo with name option", () => {
      it("parses connection info", async () => {
        findByNameMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockResolvedValueOnce("rediss://localhosta:6239");

        await expect(
          client.connectionInfo({ name: "test-redis", ownerId: "tea-abc" }),
        ).resolves.toEqual({
          host: "localhosta",
          port: 6239,
        });
      });
      it("parses connection info with username and password", async () => {
        findByNameMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockResolvedValueOnce("rediss://user:pass@localhosta:6239");

        await expect(
          client.connectionInfo({ name: "test-redis", ownerId: "tea-abc" }),
        ).resolves.toEqual({
          host: "localhosta",
          port: 6239,
          username: "user",
          password: "pass",
        });
      });
      it("errors if connection info is invalid format", async () => {
        findByNameMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockResolvedValueOnce("redis://noport.com");

        await expect(
          client.connectionInfo({ name: "test-redis", ownerId: "tea-abc" }),
        ).rejects.toThrow("an unexpected format");
      });
      it("errors if owner id is missing", async () => {
        await expect(client.connectionInfo({ name: "test-redis" })).rejects.toThrow(
          "ownerId is required",
        );
      });
      it("errors if no data returned", async () => {
        findByNameMock.mockResolvedValueOnce(null);

        await expect(
          client.connectionInfo({ name: "test-redis", ownerId: "tea-abc" }),
        ).rejects.toThrow("Unable to locate Key Value");
      });
      it("errors if connection info not found", async () => {
        const error = new Error("Unable to locate connection info");
        findByNameMock.mockResolvedValueOnce({
          id: "red-abc",
        });
        getConnectionInfoMock.mockRejectedValueOnce(error);

        await expect(
          client.connectionInfo({ name: "test-redis", ownerId: "tea-abc" }),
        ).rejects.toEqual(error);
      });
    });
  });
});
