import type { KeyValueApi } from "./api";
import { KeyValueProvider } from "./provider";
import type { OwnerId } from "./types";

describe("KeyValueProvider", () => {
  const findByIdMock = vi.fn().mockRejectedValue(new Error("findById should not be called"));
  const findByNameMock = vi.fn().mockRejectedValue(new Error("findByName should not be called"));
  const getConnectionInfoMock = vi
    .fn()
    .mockRejectedValue(new Error("getConnectionInfo should not be called"));
  const createInstanceMock = vi
    .fn()
    .mockRejectedValue(new Error("createInstance should not be called"));
  const updateInstanceMock = vi
    .fn()
    .mockRejectedValue(new Error("updateInstance should not be called"));
  const api = {
    findById: findByIdMock,
    findByName: findByNameMock,
    getConnectionInfo: getConnectionInfoMock,
    createInstance: createInstanceMock,
    updateInstance: updateInstanceMock,
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

      it("errors if no data returned and automatic provisioning is disabled", async () => {
        findByNameMock.mockResolvedValueOnce(null);

        await expect(
          client.newClient({ name: "test-redis", ownerId: "tea-abc", autoProvision: false }),
        ).rejects.toThrow("Unable to locate Key Value");
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

      it("errors if no data returned and automatic provisioning is disabled", async () => {
        findByNameMock.mockResolvedValueOnce(null);

        await expect(
          client.connectionInfo({
            name: "test-redis",
            ownerId: "tea-abc",
            autoProvision: false,
          }),
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

    describe("automatic provisioning", () => {
      beforeEach(() => {
        vi.useFakeTimers();
        findByNameMock.mockResolvedValueOnce(null);
        getConnectionInfoMock.mockResolvedValueOnce("rediss://localhosta:6239");
      });
      afterEach(() => {
        vi.clearAllMocks();
        vi.useRealTimers();
      });
      describe("for newClient", () => {
        it("sends POST request with settings from options if no instance found", async () => {
          createInstanceMock.mockRejectedValueOnce(new Error("Early exit"));

          const details = {
            name: "test-redis",
            ownerId: "tea-abc" as OwnerId,
          };

          await expect(client.newClient(details)).rejects.toBeDefined();

          expect(createInstanceMock).toHaveBeenCalledExactlyOnceWith({
            plan: "free",
            ...details,
          });
        });

        it("waits for instance to become available after creating", async () => {
          const details = {
            id: "red-abc",
            status: "creating",
          };
          createInstanceMock.mockResolvedValueOnce(details);
          findByIdMock.mockImplementation(() => {
            const response = { ...details };

            details.status = "available";

            return response;
          });

          const expectation = expect(
            client.newClient({
              name: "test-redis",
              ownerId: "tea-abc",
            }),
          ).resolves.toBeDefined();

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(2);
        });

        it("errors if instance moves to unrecoverable status", async () => {
          const details = {
            id: "red-abc",
            status: "creating",
          };
          createInstanceMock.mockResolvedValueOnce(details);
          findByIdMock.mockImplementation(() => {
            const response = { ...details };

            details.status = "recovery_failed";

            return response;
          });

          const expectation = expect(
            client.newClient({
              name: "test-redis",
              ownerId: "tea-abc",
            }),
          ).rejects.toThrow("instance is not available");

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(2);
        });
      });

      describe("for connectionInfo", () => {
        it("sends POST request with settings from options if no instance found", async () => {
          createInstanceMock.mockRejectedValueOnce(new Error("Early exit"));

          const details = {
            name: "test-redis",
            ownerId: "tea-abc" as OwnerId,
          };

          await expect(client.connectionInfo(details)).rejects.toBeDefined();

          expect(createInstanceMock).toHaveBeenCalledExactlyOnceWith({
            plan: "free",
            ...details,
          });
        });

        it("waits for instance to become available after creating", async () => {
          const details = {
            id: "red-abc",
            status: "creating",
          };
          createInstanceMock.mockResolvedValueOnce(details);
          findByIdMock.mockImplementation(() => {
            const response = { ...details };

            details.status = "available";

            return response;
          });

          const expectation = expect(
            client.connectionInfo({
              name: "test-redis",
              ownerId: "tea-abc",
            }),
          ).resolves.toEqual({
            host: "localhosta",
            port: 6239,
          });

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(2);
        });

        it("errors if instance moves to unrecoverable status", async () => {
          const details = {
            id: "red-abc",
            status: "creating",
          };
          createInstanceMock.mockResolvedValueOnce(details);
          findByIdMock.mockImplementation(() => {
            const response = { ...details };

            details.status = "recovery_failed";

            return response;
          });

          const expectation = expect(
            client.connectionInfo({
              name: "test-redis",
              ownerId: "tea-abc",
            }),
          ).rejects.toThrow("instance is not available");

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(2);
        });
      });
    });

    describe("configuration sync", () => {
      beforeEach(() => {
        vi.useFakeTimers();
        getConnectionInfoMock.mockResolvedValueOnce("rediss://user:pass@localhosta:6239");
      });
      afterEach(() => {
        vi.useRealTimers();
        vi.clearAllMocks();
      });

      describe("for newClient with service ID", () => {
        it("sends no extra requests if no settings are explicitly made", async () => {
          const details = {
            id: "red-abc",
            status: "available",
            plan: "starter",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByIdMock.mockResolvedValueOnce(details);

          await expect(client.newClient({ serviceId: "red-abc" })).resolves.toBeDefined();

          expect(updateInstanceMock).not.toHaveBeenCalled();
          expect(findByIdMock).toHaveBeenCalledOnce();
        });

        it("sends no extra requests if configuration matches request", async () => {
          const details = {
            id: "red-abc",
            status: "available",
            plan: "starter",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByIdMock.mockResolvedValueOnce(details);

          await expect(
            client.newClient({
              serviceId: "red-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_lru",
              },
            }),
          ).resolves.toBeDefined();

          expect(updateInstanceMock).not.toHaveBeenCalled();
          expect(findByIdMock).toHaveBeenCalledOnce();
        });

        it("sends PATCH request if changes are needed", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByIdMock.mockResolvedValueOnce(current);
          updateInstanceMock.mockRejectedValueOnce(new Error("early exit"));

          await expect(
            client.newClient({
              serviceId: "red-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).rejects.toBeDefined();

          expect(updateInstanceMock).toHaveBeenCalledExactlyOnceWith(current.id, {
            plan: "starter",
            maxmemoryPolicy: "allkeys_random",
          });
        });

        it("waits for instance to become available after updating", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByIdMock.mockImplementation(() => {
            const result = { ...current };

            if (current.status === "updating_instance") {
              current.status = "available";
            }

            return result;
          });
          updateInstanceMock.mockImplementationOnce(() => {
            current.plan = "starter";
            current.options.maxmemoryPolicy = "allkeys_random";
            current.status = "updating_instance";

            return { ...current };
          });

          const expectation = expect(
            client.newClient({
              serviceId: "red-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).resolves.toBeDefined();

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(3);
        });

        it("errors if instance moves to unrecoverable state", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByIdMock.mockImplementation(() => {
            const result = { ...current };

            if (current.status === "updating_instance") {
              current.status = "recovery_failed";
            }

            return result;
          });
          updateInstanceMock.mockImplementationOnce(() => {
            current.plan = "starter";
            current.options.maxmemoryPolicy = "allkeys_random";
            current.status = "updating_instance";

            return { ...current };
          });

          const expectation = expect(
            client.newClient({
              serviceId: "red-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).rejects.toThrow("instance is not available");

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(3);
        });
      });

      describe("for newClient with name & owner ID", () => {
        it("sends no extra requests if no settings are explicitly made", async () => {
          const details = {
            id: "red-abc",
            status: "available",
            plan: "starter",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByNameMock.mockResolvedValueOnce(details);

          await expect(
            client.newClient({ name: "test-redis", ownerId: "tea-abc" }),
          ).resolves.toBeDefined();

          expect(updateInstanceMock).not.toHaveBeenCalled();
          expect(findByNameMock).toHaveBeenCalledOnce();
          expect(findByIdMock).not.toHaveBeenCalled();
        });

        it("sends no extra requests if configuration matches request", async () => {
          const details = {
            id: "red-abc",
            status: "available",
            plan: "starter",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByNameMock.mockResolvedValueOnce(details);

          await expect(
            client.newClient({
              name: "test-redis",
              ownerId: "tea-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_lru",
              },
            }),
          ).resolves.toBeDefined();

          expect(updateInstanceMock).not.toHaveBeenCalled();
          expect(findByNameMock).toHaveBeenCalledOnce();
          expect(findByIdMock).not.toHaveBeenCalled();
        });

        it("sends PATCH request if changes are needed", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByNameMock.mockResolvedValueOnce(current);
          updateInstanceMock.mockRejectedValueOnce(new Error("early exit"));

          await expect(
            client.newClient({
              name: "test-redis",
              ownerId: "tea-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).rejects.toBeDefined();

          expect(updateInstanceMock).toHaveBeenCalledExactlyOnceWith(current.id, {
            plan: "starter",
            maxmemoryPolicy: "allkeys_random",
          });
        });

        it("waits for instance to become available after updating", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByNameMock.mockResolvedValueOnce({ ...current });

          findByIdMock.mockImplementation(() => {
            const result = { ...current };

            if (current.status === "updating_instance") {
              current.status = "available";
            }

            return result;
          });

          updateInstanceMock.mockImplementationOnce(() => {
            current.status = "updating_instance";
            current.plan = "starter";
            current.options.maxmemoryPolicy = "allkeys_random";

            return { ...current };
          });

          const expectation = expect(
            client.newClient({
              name: "test-redis",
              ownerId: "tea-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).resolves.toBeDefined();

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(2);
        });

        it("errors if instance moves to unrecoverable state", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByNameMock.mockResolvedValueOnce({ ...current });

          findByIdMock.mockImplementation(() => {
            const result = { ...current };

            if (current.status === "updating_instance") {
              current.status = "recovery_failed";
            }

            return result;
          });

          updateInstanceMock.mockImplementationOnce(() => {
            current.status = "updating_instance";
            current.plan = "starter";
            current.options.maxmemoryPolicy = "allkeys_random";

            return { ...current };
          });

          const expectation = expect(
            client.newClient({
              name: "test-redis",
              ownerId: "tea-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).rejects.toThrow("instance is not available");

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(2);
        });
      });

      describe("for connectionInfo with service ID", () => {
        it("sends no extra requests if no settings are explicitly made", async () => {
          const details = {
            id: "red-abc",
            status: "available",
            plan: "starter",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByIdMock.mockResolvedValueOnce(details);

          await expect(client.connectionInfo({ serviceId: "red-abc" })).resolves.toEqual({
            username: "user",
            password: "pass",
            host: "localhosta",
            port: 6239,
          });

          expect(updateInstanceMock).not.toHaveBeenCalled();
          expect(findByIdMock).toHaveBeenCalledOnce();
        });

        it("sends no extra requests if configuration matches request", async () => {
          const details = {
            id: "red-abc",
            status: "available",
            plan: "starter",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByIdMock.mockResolvedValueOnce(details);

          await expect(
            client.connectionInfo({
              serviceId: "red-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_lru",
              },
            }),
          ).resolves.toEqual({
            username: "user",
            password: "pass",
            host: "localhosta",
            port: 6239,
          });

          expect(updateInstanceMock).not.toHaveBeenCalled();
          expect(findByIdMock).toHaveBeenCalledOnce();
        });

        it("sends PATCH request if changes are needed", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByIdMock.mockResolvedValueOnce(current);
          updateInstanceMock.mockRejectedValueOnce(new Error("early exit"));

          await expect(
            client.connectionInfo({
              serviceId: "red-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).rejects.toBeDefined();

          expect(updateInstanceMock).toHaveBeenCalledExactlyOnceWith(current.id, {
            plan: "starter",
            maxmemoryPolicy: "allkeys_random",
          });
        });

        it("waits for instance to become available after updating", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByIdMock.mockImplementation(() => {
            const result = { ...current };

            if (current.status === "updating_instance") {
              current.status = "available";
            }

            return result;
          });
          updateInstanceMock.mockImplementationOnce(() => {
            current.plan = "starter";
            current.options.maxmemoryPolicy = "allkeys_random";
            current.status = "updating_instance";

            return { ...current };
          });

          const expectation = expect(
            client.connectionInfo({
              serviceId: "red-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).resolves.toEqual({
            username: "user",
            password: "pass",
            host: "localhosta",
            port: 6239,
          });

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(3);
        });

        it("errors if instance moves to unrecoverable state", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByIdMock.mockImplementation(() => {
            const result = { ...current };

            if (current.status === "updating_instance") {
              current.status = "recovery_failed";
            }

            return result;
          });
          updateInstanceMock.mockImplementationOnce(() => {
            current.plan = "starter";
            current.options.maxmemoryPolicy = "allkeys_random";
            current.status = "updating_instance";

            return { ...current };
          });

          const expectation = expect(
            client.connectionInfo({
              serviceId: "red-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).rejects.toThrow("instance is not available");

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(3);
        });
      });

      describe("for connectionInfo with name & owner ID", () => {
        it("sends no extra requests if no settings are explicitly made", async () => {
          const details = {
            id: "red-abc",
            status: "available",
            plan: "starter",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByNameMock.mockResolvedValueOnce(details);

          await expect(
            client.connectionInfo({ name: "test-redis", ownerId: "tea-abc" }),
          ).resolves.toEqual({
            username: "user",
            password: "pass",
            host: "localhosta",
            port: 6239,
          });

          expect(updateInstanceMock).not.toHaveBeenCalled();
          expect(findByNameMock).toHaveBeenCalledOnce();
          expect(findByIdMock).not.toHaveBeenCalled();
        });

        it("sends no extra requests if configuration matches request", async () => {
          const details = {
            id: "red-abc",
            status: "available",
            plan: "starter",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByNameMock.mockResolvedValueOnce(details);

          await expect(
            client.connectionInfo({
              name: "test-redis",
              ownerId: "tea-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_lru",
              },
            }),
          ).resolves.toEqual({
            username: "user",
            password: "pass",
            host: "localhosta",
            port: 6239,
          });

          expect(updateInstanceMock).not.toHaveBeenCalled();
          expect(findByNameMock).toHaveBeenCalledOnce();
          expect(findByIdMock).not.toHaveBeenCalled();
        });

        it("sends PATCH request if changes are needed", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByNameMock.mockResolvedValueOnce(current);
          updateInstanceMock.mockRejectedValueOnce(new Error("early exit"));

          await expect(
            client.connectionInfo({
              name: "test-redis",
              ownerId: "tea-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).rejects.toBeDefined();

          expect(updateInstanceMock).toHaveBeenCalledExactlyOnceWith(current.id, {
            plan: "starter",
            maxmemoryPolicy: "allkeys_random",
          });
        });

        it("waits for instance to become available after updating", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByNameMock.mockResolvedValueOnce({ ...current });

          findByIdMock.mockImplementation(() => {
            const result = { ...current };

            if (current.status === "updating_instance") {
              current.status = "available";
            }

            return result;
          });

          updateInstanceMock.mockImplementationOnce(() => {
            current.status = "updating_instance";
            current.plan = "starter";
            current.options.maxmemoryPolicy = "allkeys_random";

            return { ...current };
          });

          const expectation = expect(
            client.connectionInfo({
              name: "test-redis",
              ownerId: "tea-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).resolves.toEqual({
            username: "user",
            password: "pass",
            host: "localhosta",
            port: 6239,
          });

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(2);
        });

        it("errors if instance moves to unrecoverable state", async () => {
          const current = {
            id: "red-abc",
            status: "available",
            plan: "free",
            options: {
              maxmemoryPolicy: "allkeys_lru",
            },
            ipAllowList: [],
          };

          findByNameMock.mockResolvedValueOnce({ ...current });

          findByIdMock.mockImplementation(() => {
            const result = { ...current };

            if (current.status === "updating_instance") {
              current.status = "recovery_failed";
            }

            return result;
          });

          updateInstanceMock.mockImplementationOnce(() => {
            current.status = "updating_instance";
            current.plan = "starter";
            current.options.maxmemoryPolicy = "allkeys_random";

            return { ...current };
          });

          const expectation = expect(
            client.connectionInfo({
              name: "test-redis",
              ownerId: "tea-abc",
              autoProvision: {
                plan: "starter",
                maxmemoryPolicy: "allkeys_random",
              },
            }),
          ).rejects.toThrow("instance is not available");

          await Promise.all([expectation, vi.runAllTimersAsync()]);

          expect(findByIdMock).toHaveBeenCalledTimes(2);
        });
      });
    });
  });
});
