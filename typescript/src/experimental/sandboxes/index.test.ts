import type { Client } from "openapi-fetch";
import {
  AbortError,
  ClientError,
  RenderError,
  SandboxSnapshotNotFoundError,
  SandboxSnapshotNotReadyError,
  SandboxSnapshotPlanMismatchError,
  ServerError,
} from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import {
  type SandboxCreateInput,
  type SandboxExecEvent,
  SandboxExecStreamError,
  SandboxesClient,
  type SandboxSnapshot,
  type SandboxSnapshotWithCursor,
} from "./index.js";

function sseStream(chunks: string[]): ReadableStream<Uint8Array> {
  const encoder = new TextEncoder();
  return new ReadableStream({
    start(controller) {
      for (const chunk of chunks) {
        controller.enqueue(encoder.encode(chunk));
      }
      controller.close();
    },
  });
}

async function collect<T>(events: AsyncIterable<T>): Promise<T[]> {
  const collected: T[] = [];
  for await (const event of events) {
    collected.push(event);
  }
  return collected;
}

async function collectOpenExec(
  client: SandboxesClient,
  sandboxId: string,
  command: string,
  ownerId?: `tea-${string}`,
  signal?: AbortSignal,
): Promise<SandboxExecEvent[]> {
  const stream = await client.exec(sandboxId, command, ownerId, signal);
  return collect(stream);
}

const CONNECT_RESPONSE = {
  executionId: "exe-abc123",
  token: "connect-token",
  uri: "https://sbx-123.oregon.sandbox.onrender.com/runs/stream",
  method: "POST",
};

function mockApiClientWithConnectResponse(): Client<paths> {
  return {
    POST: vi.fn().mockResolvedValue({ data: CONNECT_RESPONSE, error: undefined }),
  } as unknown as Client<paths>;
}

type MockResult = {
  status: number;
  statusText?: string;
  error?: unknown;
  data?: unknown;
};

function mockApiClient(
  method: "GET" | "POST" | "DELETE",
  { status, statusText, error, data }: MockResult,
): Client<paths> {
  return {
    [method]: vi.fn().mockResolvedValue({
      data,
      error,
      response: new Response(null, { status, statusText }),
    }),
  } as unknown as Client<paths>;
}

const SNAPSHOT: SandboxSnapshot = {
  id: "snp-cph1rs3idesc73a2b2mg",
  sandboxGroupId: "sbg-123",
  sourceSandboxId: "sbx-123",
  kind: "filesystem",
  status: "creating",
  plan: "starter",
  requestedAt: "2026-09-01T00:00:00Z",
  capturedAt: null,
  expiresAt: "2026-09-08T00:00:00Z",
  sizeBytes: null,
  error: null,
};

const ITEM: SandboxSnapshotWithCursor = { snapshot: SNAPSHOT, cursor: "cursor-123" };

describe("SandboxesClient", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  describe("list", () => {
    it("lists sandboxes with the requested filters", async () => {
      const sandboxes = [
        {
          sandbox: {
            id: "sbx-123",
            status: "running",
            plan: "standard",
            networkPolicy: { default: "deny-all" },
            region: "oregon",
            timeoutSeconds: 300,
            createdAt: "2026-08-12T00:00:00Z",
            terminatedAt: null,
          },
          cursor: "cursor-123",
        },
      ];
      const apiClient = {
        GET: vi.fn().mockResolvedValue({ data: sandboxes, error: undefined }),
      } as unknown as Client<paths>;
      const client = new SandboxesClient(apiClient);

      await expect(
        client.list({
          ownerId: "tea-test",
          cursor: "cursor-before",
          limit: 25,
          status: ["running"],
        }),
      ).resolves.toEqual(sandboxes);
      expect(apiClient.GET).toHaveBeenCalledWith("/sandboxes", {
        params: {
          query: {
            ownerId: "tea-test",
            cursor: "cursor-before",
            limit: 25,
            status: ["running"],
          },
        },
      });
    });

    it("uses client defaults when called without options", async () => {
      const apiClient = {
        GET: vi.fn().mockResolvedValue({ data: [], error: undefined }),
      } as unknown as Client<paths>;
      const client = new SandboxesClient(apiClient, "tea-default");

      await expect(client.list()).resolves.toEqual([]);
      expect(apiClient.GET).toHaveBeenCalledWith("/sandboxes", {
        params: {
          query: {
            ownerId: "tea-default",
            cursor: undefined,
            limit: undefined,
            status: undefined,
          },
        },
      });
    });
  });

  describe("listGroups", () => {
    const GROUP = {
      sandboxGroup: {
        id: "sbg-123",
        ownerId: "tea-test",
        name: "Default",
        region: "oregon",
        isDefault: true,
        environmentId: null,
        concurrencyLimit: 10,
        createdAt: "2026-07-02T18:30:00Z",
        updatedAt: "2026-07-02T18:30:00Z",
      },
      cursor: "cursor-123",
    };

    it("lists sandbox groups for the requested owner", async () => {
      const apiClient = {
        GET: vi.fn().mockResolvedValue({ data: [GROUP], error: undefined }),
      } as unknown as Client<paths>;
      const client = new SandboxesClient(apiClient, "tea-default");

      await expect(client.listGroups({ ownerId: "tea-test" })).resolves.toEqual([GROUP]);
      expect(apiClient.GET).toHaveBeenCalledWith("/sandbox-groups", {
        params: { query: { ownerId: "tea-test" } },
      });
    });

    it("uses the client default owner when called without options", async () => {
      const apiClient = {
        GET: vi.fn().mockResolvedValue({ data: [], error: undefined }),
      } as unknown as Client<paths>;
      const client = new SandboxesClient(apiClient, "tea-default");

      await expect(client.listGroups()).resolves.toEqual([]);
      expect(apiClient.GET).toHaveBeenCalledWith("/sandbox-groups", {
        params: { query: { ownerId: "tea-default" } },
      });
    });

    it("requires an owner ID", async () => {
      const apiClient = { GET: vi.fn() } as unknown as Client<paths>;
      const client = new SandboxesClient(apiClient);

      await expect(client.listGroups()).rejects.toBeInstanceOf(RenderError);
      expect(apiClient.GET).not.toHaveBeenCalled();
    });

    it("throws ClientError when the API rejects the request", async () => {
      const apiClient = {
        GET: vi.fn().mockResolvedValue({
          data: undefined,
          error: { message: "workspace not found" },
          response: new Response(null, { status: 404 }),
        }),
      } as unknown as Client<paths>;
      const client = new SandboxesClient(apiClient, "tea-default");

      const error = await client.listGroups().catch((err) => err);
      expect(error).toBeInstanceOf(ClientError);
      expect(error).toMatchObject({
        statusCode: 404,
        message: "Failed to list sandbox groups: workspace not found",
      });
    });
  });

  describe("create", () => {
    it("passes caller-supplied options and falls back to the client region", async () => {
      const sandbox = { id: "sbx-123" };
      const apiClient = {
        POST: vi.fn().mockResolvedValue({
          data: sandbox,
          error: undefined,
          response: new Response(null, { status: 201 }),
        }),
      } as unknown as Client<paths>;
      const client = new SandboxesClient(apiClient, "tea-default", "oregon");

      await expect(
        client.create({
          plan: "pro",
          timeoutSeconds: 600,
          networkPolicy: { default: "deny-all" },
          env: { NODE_ENV: "test" },
        }),
      ).resolves.toEqual(sandbox);
      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: {
          ownerId: "tea-default",
          plan: "pro",
          timeoutSeconds: 600,
          region: "oregon",
          networkPolicy: { default: "deny-all" },
          env: { NODE_ENV: "test" },
        },
      });
    });

    it("omits options that should use API defaults", async () => {
      const apiClient = {
        POST: vi.fn().mockResolvedValue({
          data: { id: "sbx-123" },
          error: undefined,
          response: new Response(null, { status: 201 }),
        }),
      } as unknown as Client<paths>;
      const client = new SandboxesClient(apiClient);

      await client.create({ ownerId: "tea-test" });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test" },
      });
    });

    it("forwards the snapshot ID", async () => {
      const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
      const client = new SandboxesClient(apiClient);

      await client.create({ ownerId: "tea-test", snapshotId: "snp-cph1rs3idesc73a2b2mg" });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test", snapshotId: "snp-cph1rs3idesc73a2b2mg" },
      });
    });

    const createErrorRows: {
      status: number;
      code: string | undefined;
      input: SandboxCreateInput;
      ErrorClass: typeof ClientError;
    }[] = [
      {
        status: 404,
        code: "snapshot_not_found",
        input: { snapshotId: "snp-missing" },
        ErrorClass: SandboxSnapshotNotFoundError,
      },
      {
        status: 404,
        code: undefined,
        input: { snapshotId: "snp-missing" },
        ErrorClass: ClientError,
      },
      { status: 404, code: undefined, input: {}, ErrorClass: ClientError },
      {
        status: 409,
        code: "snapshot_not_available",
        input: { snapshotId: "snp-creating" },
        ErrorClass: SandboxSnapshotNotReadyError,
      },
      {
        status: 409,
        code: "snapshot_plan_mismatch",
        input: { snapshotId: "snp-runtime", plan: "pro" },
        ErrorClass: SandboxSnapshotPlanMismatchError,
      },
    ];

    it.each(createErrorRows)(
      "maps $status with code $code to $ErrorClass.name for $input",
      async ({ status, code, input, ErrorClass }) => {
        const apiClient = mockApiClient("POST", { status, error: { message: "rejected", code } });
        const client = new SandboxesClient(apiClient, "tea-default");

        const error = await client.create(input).catch((err) => err);
        expect(error.constructor).toBe(ErrorClass);
        expect(error).toMatchObject({
          statusCode: status,
          code,
          message: "Failed to create sandbox: rejected",
        });
      },
    );

    it.each([undefined, ""])("rejects a bodyless non-2xx with error %j", async (body) => {
      const apiClient = mockApiClient("POST", {
        status: 404,
        statusText: "Not Found",
        error: body,
      });
      const client = new SandboxesClient(apiClient, "tea-default");

      const error = await client.create({ snapshotId: "snp-missing" }).catch((err) => err);
      expect(error.constructor).toBe(ClientError);
      expect(error.code).toBeUndefined();
      expect(error).toMatchObject({
        statusCode: 404,
        message: "Failed to create sandbox: Not Found",
      });
    });
  });

  describe("snapshots", () => {
    const GROUP_SNAPSHOT_PATH = "/sandbox-groups/{sandboxGroupId}/snapshots/{snapshotId}";
    const groupSnapshotInput = { sandboxGroupId: "sbg-123", snapshotId: SNAPSHOT.id };

    const ownerlessRows: {
      op: string;
      method: "GET" | "POST" | "DELETE";
      status: number;
      call: (client: SandboxesClient) => Promise<unknown>;
      path: string;
      params: Record<string, unknown>;
    }[] = [
      {
        op: "create",
        method: "POST",
        status: 202,
        call: (client) => client.snapshots.create({ sandboxId: "sbx-123" }),
        path: "/sandboxes/{sandboxId}/snapshots",
        params: { path: { sandboxId: "sbx-123" } },
      },
      {
        op: "get",
        method: "GET",
        status: 200,
        call: (client) => client.snapshots.get(groupSnapshotInput),
        path: GROUP_SNAPSHOT_PATH,
        params: { path: groupSnapshotInput },
      },
      {
        op: "delete",
        method: "DELETE",
        status: 204,
        call: (client) => client.snapshots.delete(groupSnapshotInput),
        path: GROUP_SNAPSHOT_PATH,
        params: { path: groupSnapshotInput },
      },
    ];

    it.each(ownerlessRows)(
      "$op omits ownerId when none is configured",
      async ({ method, status, call, path, params }) => {
        const apiClient = mockApiClient(method, { status, data: SNAPSHOT });
        const client = new SandboxesClient(apiClient);

        await call(client);

        expect(apiClient[method]).toHaveBeenCalledWith(path, { params });
      },
    );

    const groupErrorRows: {
      op: string;
      method: "GET" | "DELETE";
      status: number;
      code: string | undefined;
      call: (client: SandboxesClient) => Promise<unknown>;
      ErrorClass: typeof ClientError;
      context: string;
    }[] = [
      {
        op: "get",
        method: "GET",
        status: 404,
        code: undefined,
        call: (client) => client.snapshots.get(groupSnapshotInput),
        ErrorClass: SandboxSnapshotNotFoundError,
        context: "Failed to get snapshot",
      },
      {
        op: "list",
        method: "GET",
        status: 404,
        code: undefined,
        call: (client) => client.snapshots.list({ sandboxGroupId: "sbg-123" }),
        ErrorClass: ClientError,
        context: "Failed to list snapshots",
      },
      {
        op: "delete",
        method: "DELETE",
        status: 404,
        code: undefined,
        call: (client) => client.snapshots.delete(groupSnapshotInput),
        ErrorClass: SandboxSnapshotNotFoundError,
        context: "Failed to delete snapshot",
      },
      {
        op: "delete",
        method: "DELETE",
        status: 409,
        code: "snapshot_creating",
        call: (client) => client.snapshots.delete(groupSnapshotInput),
        ErrorClass: SandboxSnapshotNotReadyError,
        context: "Failed to delete snapshot",
      },
    ];

    it.each(groupErrorRows)(
      "$op maps $status with code $code to $ErrorClass.name",
      async ({ method, status, code, call, ErrorClass, context }) => {
        const apiClient = mockApiClient(method, { status, error: { message: "rejected", code } });
        const client = new SandboxesClient(apiClient, "tea-default");

        const error = await call(client).catch((err) => err);
        expect(Object.getPrototypeOf(error)).toBe(ErrorClass.prototype);
        expect(error).toMatchObject({ statusCode: status, code, message: `${context}: rejected` });
      },
    );

    describe("create", () => {
      it("captures a snapshot of the requested kind", async () => {
        const apiClient = mockApiClient("POST", { status: 202, data: SNAPSHOT });
        const client = new SandboxesClient(apiClient, "tea-default");

        await expect(
          client.snapshots.create({ sandboxId: "sbx-123", kind: "runtime", ownerId: "tea-test" }),
        ).resolves.toEqual(SNAPSHOT);
        expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes/{sandboxId}/snapshots", {
          params: { path: { sandboxId: "sbx-123" }, query: { ownerId: "tea-test" } },
          body: { kind: "runtime" },
        });
      });

      it("omits the body so the API applies the default kind", async () => {
        const apiClient = mockApiClient("POST", { status: 202, data: SNAPSHOT });
        const client = new SandboxesClient(apiClient, "tea-default");

        await client.snapshots.create({ sandboxId: "sbx-123" });

        expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes/{sandboxId}/snapshots", {
          params: { path: { sandboxId: "sbx-123" }, query: { ownerId: "tea-default" } },
        });
      });

      it("sends expiresAt so the API applies the requested lifetime", async () => {
        const apiClient = mockApiClient("POST", { status: 202, data: SNAPSHOT });
        const client = new SandboxesClient(apiClient, "tea-default");

        await client.snapshots.create({
          sandboxId: "sbx-123",
          expiresAt: "2026-09-08T00:00:00Z",
        });

        expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes/{sandboxId}/snapshots", {
          params: { path: { sandboxId: "sbx-123" }, query: { ownerId: "tea-default" } },
          body: { expiresAt: "2026-09-08T00:00:00Z" },
        });
      });

      const codeRows: {
        status: number;
        code: string | undefined;
        ErrorClass: typeof ClientError | typeof ServerError;
      }[] = [
        { status: 409, code: "snapshot_creating", ErrorClass: SandboxSnapshotNotReadyError },
        { status: 409, code: "snapshot_not_available", ErrorClass: SandboxSnapshotNotReadyError },
        {
          status: 409,
          code: "snapshot_plan_mismatch",
          ErrorClass: SandboxSnapshotPlanMismatchError,
        },
        { status: 404, code: "snapshot_not_found", ErrorClass: SandboxSnapshotNotFoundError },
        { status: 409, code: "sandbox_not_running", ErrorClass: ClientError },
        { status: 409, code: undefined, ErrorClass: ClientError },
        { status: 404, code: undefined, ErrorClass: ClientError },
        { status: 500, code: "snapshot_creating", ErrorClass: ServerError },
      ];

      it.each(codeRows)(
        "maps $status with code $code to $ErrorClass.name",
        async ({ status, code, ErrorClass }) => {
          const apiClient = mockApiClient("POST", { status, error: { message: "rejected", code } });
          const client = new SandboxesClient(apiClient, "tea-default");

          const error = await client.snapshots.create({ sandboxId: "sbx-123" }).catch((err) => err);
          expect(error.constructor).toBe(ErrorClass);
          expect(error).toMatchObject({
            statusCode: status,
            message: "Failed to create snapshot: rejected",
          });
        },
      );

      it.each([undefined, ""])("rejects a bodyless non-2xx with error %j", async (body) => {
        const apiClient = mockApiClient("POST", {
          status: 409,
          statusText: "Conflict",
          error: body,
        });
        const client = new SandboxesClient(apiClient, "tea-default");

        const error = await client.snapshots.create({ sandboxId: "sbx-123" }).catch((err) => err);
        expect(error.constructor).toBe(ClientError);
        expect(error.code).toBeUndefined();
        expect(error).toMatchObject({
          statusCode: 409,
          message: "Failed to create snapshot: Conflict",
        });
      });
    });

    describe("get", () => {
      it("retrieves a snapshot by group and ID", async () => {
        const apiClient = mockApiClient("GET", { status: 200, data: SNAPSHOT });
        const client = new SandboxesClient(apiClient, "tea-default");

        await expect(
          client.snapshots.get({ sandboxGroupId: "sbg-123", snapshotId: SNAPSHOT.id }),
        ).resolves.toEqual(SNAPSHOT);
        expect(apiClient.GET).toHaveBeenCalledWith(
          "/sandbox-groups/{sandboxGroupId}/snapshots/{snapshotId}",
          {
            params: {
              path: { sandboxGroupId: "sbg-123", snapshotId: SNAPSHOT.id },
              query: { ownerId: "tea-default" },
            },
          },
        );
      });
    });

    describe("list", () => {
      it("lists snapshots in a sandbox group with the requested filters", async () => {
        const apiClient = mockApiClient("GET", { status: 200, data: [ITEM] });
        const client = new SandboxesClient(apiClient, "tea-default");

        await expect(
          client.snapshots.list({
            sandboxGroupId: "sbg-123",
            status: ["available"],
            cursor: "cursor-before",
            limit: 10,
            ownerId: "tea-test",
          }),
        ).resolves.toEqual([ITEM]);
        expect(apiClient.GET).toHaveBeenCalledWith("/sandbox-groups/{sandboxGroupId}/snapshots", {
          params: {
            path: { sandboxGroupId: "sbg-123" },
            query: {
              ownerId: "tea-test",
              status: ["available"],
              cursor: "cursor-before",
              limit: 10,
            },
          },
        });
      });

      it("requires an owner ID", async () => {
        const apiClient = { GET: vi.fn() } as unknown as Client<paths>;
        const client = new SandboxesClient(apiClient);

        await expect(client.snapshots.list({ sandboxGroupId: "sbg-123" })).rejects.toBeInstanceOf(
          RenderError,
        );
        expect(apiClient.GET).not.toHaveBeenCalled();
      });
    });

    describe("delete", () => {
      it("deletes a snapshot", async () => {
        const apiClient = mockApiClient("DELETE", { status: 204 });
        const client = new SandboxesClient(apiClient, "tea-default");

        await expect(
          client.snapshots.delete({
            sandboxGroupId: "sbg-123",
            snapshotId: SNAPSHOT.id,
            ownerId: "tea-test",
          }),
        ).resolves.toBeUndefined();
        expect(apiClient.DELETE).toHaveBeenCalledWith(
          "/sandbox-groups/{sandboxGroupId}/snapshots/{snapshotId}",
          {
            params: {
              path: { sandboxGroupId: "sbg-123", snapshotId: SNAPSHOT.id },
              query: { ownerId: "tea-test" },
            },
          },
        );
      });
    });
  });

  describe("files", () => {
    it("uploads bytes through a file connect token", async () => {
      const connection = {
        ...CONNECT_RESPONSE,
        uri: "https://proxy.test/files/upload",
        method: "PUT",
      };
      const apiClient = {
        POST: vi.fn().mockResolvedValue({ data: connection, error: undefined }),
      } as unknown as Client<paths>;
      const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(null));
      const client = new SandboxesClient(apiClient);
      const contents = Buffer.from("hello");

      await client.upload("sbx-123", "/app/hello.txt", contents, "tea-test");

      expect(apiClient.POST).toHaveBeenCalledWith(
        "/sandboxes/{sandboxId}/files/{operation}/token",
        {
          params: {
            path: { sandboxId: "sbx-123", operation: "upload" },
            query: { ownerId: "tea-test", path: "/app/hello.txt" },
          },
        },
      );
      expect(fetchMock).toHaveBeenCalledWith(
        connection.uri,
        expect.objectContaining({
          method: "PUT",
          body: contents,
          headers: expect.objectContaining({
            Authorization: `Bearer ${connection.token}`,
            "Content-Type": "application/octet-stream",
          }),
        }),
      );
    });

    it("throws AbortError when reading an upload error response is aborted", async () => {
      const apiClient = {
        POST: vi.fn().mockResolvedValue({ data: CONNECT_RESPONSE, error: undefined }),
      } as unknown as Client<paths>;
      const response = new Response(null, { status: 500 });
      vi.spyOn(response, "text").mockRejectedValue(
        new DOMException("This operation was aborted", "AbortError"),
      );
      vi.spyOn(globalThis, "fetch").mockResolvedValue(response);
      const client = new SandboxesClient(apiClient);

      await expect(
        client.upload("sbx-123", "/app/hello.txt", Buffer.from("hello"), "tea-test"),
      ).rejects.toBeInstanceOf(AbortError);
    });

    it("downloads bytes through a file connect token", async () => {
      const connection = {
        ...CONNECT_RESPONSE,
        uri: "https://proxy.test/files/download",
        method: "GET",
      };
      const apiClient = {
        POST: vi.fn().mockResolvedValue({ data: connection, error: undefined }),
      } as unknown as Client<paths>;
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response("hello", {
          headers: { "Content-Type": "application/octet-stream" },
        }),
      );
      const client = new SandboxesClient(apiClient);

      const downloaded = await client.download("sbx-123", "/app/hello.txt", "tea-test");

      expect(apiClient.POST).toHaveBeenCalledWith(
        "/sandboxes/{sandboxId}/files/{operation}/token",
        {
          params: {
            path: { sandboxId: "sbx-123", operation: "download" },
            query: { ownerId: "tea-test", path: "/app/hello.txt" },
          },
        },
      );
      expect(downloaded).toEqual({
        data: Buffer.from("hello"),
        size: 5,
        contentType: "application/octet-stream",
      });
    });

    it("throws AbortError when reading the download body is aborted", async () => {
      const apiClient = {
        POST: vi.fn().mockResolvedValue({ data: CONNECT_RESPONSE, error: undefined }),
      } as unknown as Client<paths>;
      const response = new Response();
      vi.spyOn(response, "arrayBuffer").mockRejectedValue(
        new DOMException("This operation was aborted", "AbortError"),
      );
      vi.spyOn(globalThis, "fetch").mockResolvedValue(response);
      const client = new SandboxesClient(apiClient);

      await expect(client.download("sbx-123", "/app/hello.txt", "tea-test")).rejects.toBeInstanceOf(
        AbortError,
      );
    });
  });

  describe("openExec", () => {
    it("streams output events until the exit event", async () => {
      const apiClient = mockApiClientWithConnectResponse();
      const fetchMock = vi
        .spyOn(globalThis, "fetch")
        .mockResolvedValue(
          new Response(
            sseStream([
              'event: output\ndata: {"stream":"stdout","data":"hi\\n"}\n\n',
              'event: output\ndata: {"stream":"stderr","data":"warn\\n"}\n\n',
              'event: exit\ndata: {"exit_code":7}\n\n',
            ]),
            { status: 200 },
          ),
        );
      const client = new SandboxesClient(apiClient);

      expect(await collectOpenExec(client, "sbx-123", "echo hi", "tea-test")).toEqual([
        { type: "output", stream: "stdout", data: "hi\n" },
        { type: "output", stream: "stderr", data: "warn\n" },
        { type: "exit", exit_code: 7 },
      ]);

      expect(apiClient.POST).toHaveBeenCalledWith(
        "/sandboxes/{sandboxId}/runs/{operation}/token",
        expect.objectContaining({
          params: {
            path: { sandboxId: "sbx-123", operation: "stream" },
            query: { ownerId: "tea-test" },
          },
          body: { command: "echo hi" },
        }),
      );
      expect(fetchMock).toHaveBeenCalledWith(
        CONNECT_RESPONSE.uri,
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ command: "echo hi" }),
          headers: expect.objectContaining({
            Accept: "text/event-stream",
            Authorization: `Bearer ${CONNECT_RESPONSE.token}`,
            "Content-Type": "application/json",
          }),
        }),
      );
    });

    it("omits the connect token body when the command is empty", async () => {
      const apiClient = mockApiClientWithConnectResponse();
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response(sseStream(['event: exit\ndata: {"exit_code":0}\n\n']), { status: 200 }),
      );
      const client = new SandboxesClient(apiClient);

      await collectOpenExec(client, "sbx-123", "", "tea-test");

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes/{sandboxId}/runs/{operation}/token", {
        params: {
          path: { sandboxId: "sbx-123", operation: "stream" },
          query: { ownerId: "tea-test" },
        },
      });
    });

    it("joins multi-line data fields", async () => {
      const apiClient = mockApiClientWithConnectResponse();
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response(sseStream(['event: exit\ndata: {"exit_code":\ndata: 3}\n\n']), {
          status: 200,
        }),
      );
      const client = new SandboxesClient(apiClient);

      await expect(collectOpenExec(client, "sbx-123", "echo hi", "tea-test")).resolves.toEqual([
        { type: "exit", exit_code: 3 },
      ]);
    });

    it("throws SandboxExecStreamError for terminal error events", async () => {
      const apiClient = mockApiClientWithConnectResponse();
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response(
          sseStream([
            'event: output\ndata: {"stream":"stdout","data":"started"}\n\n',
            'event: error\ndata: {"status":408,"message":"exec timed out"}\n\n',
          ]),
          { status: 200 },
        ),
      );
      const client = new SandboxesClient(apiClient);

      let error: unknown;
      try {
        await collectOpenExec(client, "sbx-123", "sleep 999", "tea-test");
      } catch (err) {
        error = err;
      }
      expect(error).toBeInstanceOf(SandboxExecStreamError);
      expect(error).toMatchObject({
        status: 408,
        message: "exec timed out",
      });
    });

    it("throws when the stream ends without a terminal event", async () => {
      const apiClient = mockApiClientWithConnectResponse();
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response(sseStream(['event: output\ndata: {"stream":"stdout","data":"hi"}\n\n']), {
          status: 200,
        }),
      );
      const client = new SandboxesClient(apiClient);

      await expect(collectOpenExec(client, "sbx-123", "echo hi", "tea-test")).rejects.toThrow(
        "Sandbox exec stream ended without a terminal event.",
      );
    });

    it("throws ClientError for non-2xx responses before returning a stream", async () => {
      const apiClient = mockApiClientWithConnectResponse();
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response("sandbox not ready", { status: 400, statusText: "Bad Request" }),
      );
      const client = new SandboxesClient(apiClient);

      let error: unknown;
      try {
        await client.exec("sbx-123", "echo hi", "tea-test");
      } catch (err) {
        error = err;
      }
      expect(error).toBeInstanceOf(ClientError);
      expect(error).toMatchObject({
        message: "Failed to execute sandbox command: sandbox not ready",
      });
    });

    it("throws ClientError when the connect token request fails", async () => {
      const apiClient = {
        POST: vi.fn().mockResolvedValue({
          data: undefined,
          error: { message: "boom" },
          response: new Response(null, { status: 404 }),
        }),
      } as unknown as Client<paths>;
      const fetchMock = vi.spyOn(globalThis, "fetch");
      const client = new SandboxesClient(apiClient);

      const error = await collectOpenExec(client, "sbx-123", "echo hi", "tea-test").catch(
        (err) => err,
      );
      expect(error).toBeInstanceOf(RenderError);
      expect(error).toBeInstanceOf(ClientError);
      expect(error).toMatchObject({
        statusCode: 404,
        message: "Failed to get connect token: boom",
      });
      expect(fetchMock).not.toHaveBeenCalled();
    });

    it("throws AbortError if the signal is already aborted", async () => {
      const apiClient = mockApiClientWithConnectResponse();
      const fetchMock = vi.spyOn(globalThis, "fetch");
      const client = new SandboxesClient(apiClient);
      const controller = new AbortController();
      controller.abort();

      await expect(
        collectOpenExec(client, "sbx-123", "echo hi", "tea-test", controller.signal),
      ).rejects.toBeInstanceOf(AbortError);
      expect(fetchMock).not.toHaveBeenCalled();
      expect(apiClient.POST).not.toHaveBeenCalled();
    });

    it("requires an owner ID", async () => {
      const apiClient = mockApiClientWithConnectResponse();
      const fetchMock = vi.spyOn(globalThis, "fetch");
      const client = new SandboxesClient(apiClient);

      await expect(collectOpenExec(client, "sbx-123", "echo hi")).rejects.toBeInstanceOf(
        RenderError,
      );
      expect(fetchMock).not.toHaveBeenCalled();
    });
  });

  describe("exec", () => {
    it("releases the response body when the caller stops consuming early", async () => {
      const apiClient = mockApiClientWithConnectResponse();
      let cancelled = false;
      const encoder = new TextEncoder();
      const body = new ReadableStream<Uint8Array>({
        start(controller) {
          controller.enqueue(
            encoder.encode('event: output\ndata: {"stream":"stdout","data":"a\\n"}\n\n'),
          );
        },
        cancel() {
          cancelled = true;
        },
      });
      vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(body, { status: 200 }));
      const client = new SandboxesClient(apiClient);

      const stream = await client.exec("sbx-123", "tail -f log", "tea-test");
      for await (const event of stream) {
        if (event.type === "output") break;
      }

      expect(cancelled).toBe(true);
      expect(body.locked).toBe(false);
    });

    it("streams exec events", async () => {
      const apiClient = mockApiClientWithConnectResponse();
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response(sseStream(['event: exit\ndata: {"exit_code":0}\n\n']), { status: 200 }),
      );
      const client = new SandboxesClient(apiClient);

      await expect(collect(await client.exec("sbx-123", "echo hi", "tea-test"))).resolves.toEqual([
        { type: "exit", exit_code: 0 },
      ]);
    });
  });
});
