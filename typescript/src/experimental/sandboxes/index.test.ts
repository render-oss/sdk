import type { Client } from "openapi-fetch";
import {
  AbortError,
  ClientError,
  RenderError,
  SandboxBuildNotFoundError,
  SandboxBuildNotReadyError,
  SandboxCreateWaitError,
  SandboxEndedError,
  SandboxImageFailedError,
  SandboxImageNotFoundError,
  SandboxImageNotReadyError,
  SandboxImageWaitTimeoutError,
  SandboxNotRunningError,
  SandboxSnapshotCreateWaitError,
  SandboxSnapshotFailedError,
  SandboxSnapshotNotFoundError,
  SandboxSnapshotNotReadyError,
  SandboxSnapshotPlanMismatchError,
  SandboxSnapshotWaitTimeoutError,
  SandboxWaitTimeoutError,
  ServerError,
  TimeoutError,
} from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import {
  type SandboxBuild,
  type SandboxCreateInput,
  type SandboxExecEvent,
  SandboxExecStreamError,
  SandboxesClient,
  type SandboxImage,
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
    POST: vi.fn().mockResolvedValue({
      data: CONNECT_RESPONSE,
      error: undefined,
      response: new Response(null, { status: 200 }),
    }),
  } as unknown as Client<paths>;
}

type MockResult = {
  status: number;
  statusText?: string;
  error?: unknown;
  data?: unknown;
};

function mockApiClient(
  method: "GET" | "POST" | "PATCH" | "DELETE",
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
  name: null,
  kind: "filesystem",
  status: "creating",
  plan: "1c-2g",
  requestedAt: "2026-09-01T00:00:00Z",
  capturedAt: null,
  expiresAt: "2026-09-08T00:00:00Z",
  sizeBytes: null,
  error: null,
};

const ITEM: SandboxSnapshotWithCursor = { snapshot: SNAPSHOT, cursor: "cursor-123" };

const IMAGE: SandboxImage = {
  id: "sbb-cph1rs3idesc73a2b2mg",
  sandboxGroupId: "sbg-123",
  name: "python",
  source: { repository: "docker.io/library", image: "python", reference: "3.13" },
  sourceDigest: "sha256:c19d4a1",
  status: "running",
  failureReason: null,
  createdAt: "2026-10-01T00:00:00Z",
  finishedAt: null,
};

const IMAGE_IMPORT_INPUT = {
  sandboxGroupId: "sbg-123",
  name: "python",
  source: "python:3.13",
};

describe("SandboxesClient", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  describe("error responses without a body", () => {
    const calls: Array<{
      name: string;
      method: "GET" | "POST";
      context: string;
      call: (client: SandboxesClient) => Promise<unknown>;
    }> = [
      {
        name: "get",
        method: "GET",
        context: "Failed to get sandbox",
        call: (c) => c.get("sbx-123"),
      },
      {
        name: "list",
        method: "GET",
        context: "Failed to list sandboxes in workspace tea-default",
        call: (c) => c.list(),
      },
      {
        name: "listGroups",
        method: "GET",
        context: "Failed to list sandbox groups in workspace tea-default",
        call: (c) => c.listGroups(),
      },
      {
        name: "terminate",
        method: "POST",
        context: "Failed to terminate sandbox",
        call: (c) => c.terminate("sbx-123"),
      },
      {
        name: "upload",
        method: "POST",
        context: "Failed to get file connect token",
        call: (c) => c.upload("sbx-123", "/root/a.txt", "hi"),
      },
      {
        name: "download",
        method: "POST",
        context: "Failed to get file connect token",
        call: (c) => c.download("sbx-123", "/root/a.txt"),
      },
      {
        name: "exec",
        method: "POST",
        context: "Failed to get connect token",
        call: (c) => c.exec("sbx-123", "echo hi").then((events) => collect(events)),
      },
      {
        name: "images.import",
        method: "POST",
        context: "Failed to import image",
        call: (c) => c.images.import(IMAGE_IMPORT_INPUT),
      },
      {
        name: "images.get",
        method: "GET",
        context: "Failed to get image",
        call: (c) => c.images.get({ sandboxGroupId: "sbg-123", imageId: IMAGE.id }),
      },
    ];

    for (const { name, method, context, call } of calls) {
      for (const [status, ErrorClass] of [
        [503, ServerError],
        [404, ClientError],
      ] as const) {
        it(`${name} throws ${ErrorClass.name} for a bodiless ${status}`, async () => {
          const fetchMock = vi.spyOn(globalThis, "fetch");
          const client = new SandboxesClient(
            mockApiClient(method, { status, statusText: "Upstream Failure" }),
            "tea-default",
          );

          const error = await call(client).catch((err) => err);
          expect(error).toBeInstanceOf(ErrorClass);
          expect(error).toMatchObject({
            statusCode: status,
            message: `${context}: Upstream Failure`,
          });
          expect(fetchMock).not.toHaveBeenCalled();
        });
      }
    }
  });

  describe("list", () => {
    it("lists sandboxes with the requested filters", async () => {
      const sandboxes = [
        {
          sandbox: {
            id: "sbx-123",
            status: "running",
            plan: "2c-4g",
            networkPolicy: { type: "deny-all" },
            region: "oregon",
            timeoutSeconds: 300,
            createdAt: "2026-08-12T00:00:00Z",
            terminatedAt: null,
          },
          cursor: "cursor-123",
        },
      ];
      const apiClient = {
        GET: vi.fn().mockResolvedValue({
          data: sandboxes,
          error: undefined,
          response: new Response(null, { status: 200 }),
        }),
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
        GET: vi.fn().mockResolvedValue({
          data: [],
          error: undefined,
          response: new Response(null, { status: 200 }),
        }),
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
        GET: vi.fn().mockResolvedValue({
          data: [GROUP],
          error: undefined,
          response: new Response(null, { status: 200 }),
        }),
      } as unknown as Client<paths>;
      const client = new SandboxesClient(apiClient, "tea-default");

      await expect(client.listGroups({ ownerId: "tea-test" })).resolves.toEqual([GROUP]);
      expect(apiClient.GET).toHaveBeenCalledWith("/sandbox-groups", {
        params: { query: { ownerId: "tea-test" } },
      });
    });

    it("uses the client default owner when called without options", async () => {
      const apiClient = {
        GET: vi.fn().mockResolvedValue({
          data: [],
          error: undefined,
          response: new Response(null, { status: 200 }),
        }),
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
        message: "Failed to list sandbox groups in workspace tea-default: workspace not found",
      });
    });
  });

  describe("terminate", () => {
    it("terminates a sandbox when the API answers 204 with no body", async () => {
      const apiClient = mockApiClient("POST", { status: 204 });
      const client = new SandboxesClient(apiClient, "tea-default");

      await expect(client.terminate("sbx-123", "tea-test")).resolves.toBeUndefined();
      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes/{sandboxId}/terminate", {
        params: {
          path: { sandboxId: "sbx-123" },
          query: { ownerId: "tea-test" },
        },
      });
    });
  });

  describe("create", () => {
    it.each([
      { type: "deny-all" as const },
      { type: "allow-all" as const },
      { type: "allow-list" as const, rules: [] },
      {
        type: "allow-list" as const,
        rules: [{ domain: "example.com", protocol: "https" as const }],
      },
    ])("forwards network policy %j", async (networkPolicy) => {
      const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
      const client = new SandboxesClient(apiClient, "tea-test");

      await client.create({ networkPolicy });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test", networkPolicy },
      });
    });

    it("accepts and forwards a plan unknown to the SDK", async () => {
      expectTypeOf<{ plan: "32c-64g" }>().toExtend<SandboxCreateInput>();
      const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
      const client = new SandboxesClient(apiClient, "tea-test");

      await client.create({ plan: "32c-64g" });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test", plan: "32c-64g" },
      });
    });

    it("keeps snapshot ID and snapshot name mutually exclusive in the public type", () => {
      expectTypeOf<{ snapshotId: string }>().toExtend<SandboxCreateInput>();
      expectTypeOf<{ snapshotName: string }>().toExtend<SandboxCreateInput>();
      expectTypeOf<{
        snapshotId: string;
        snapshotName: string;
      }>().not.toExtend<SandboxCreateInput>();
    });

    it("keeps an image mutually exclusive with every other source in the public type", () => {
      expectTypeOf<{ image: string }>().toExtend<SandboxCreateInput>();
      expectTypeOf<{ image: string; snapshotId: string }>().not.toExtend<SandboxCreateInput>();
      expectTypeOf<{ image: string; snapshotName: string }>().not.toExtend<SandboxCreateInput>();
      expectTypeOf<{ image: string; buildId: string }>().not.toExtend<SandboxCreateInput>();
      expectTypeOf<{ image: string; buildName: string }>().not.toExtend<SandboxCreateInput>();
    });

    it("keeps a deprecated build mutually exclusive with every other source", () => {
      expectTypeOf<{ buildId: string }>().toExtend<SandboxCreateInput>();
      expectTypeOf<{ buildName: string }>().toExtend<SandboxCreateInput>();
      expectTypeOf<{ buildId: string; buildName: string }>().not.toExtend<SandboxCreateInput>();
      expectTypeOf<{ buildId: string; snapshotId: string }>().not.toExtend<SandboxCreateInput>();
      expectTypeOf<{
        buildName: string;
        snapshotName: string;
      }>().not.toExtend<SandboxCreateInput>();
    });

    it("requires rules for an allow-list network policy and rejects them otherwise", () => {
      expectTypeOf<{
        networkPolicy: { type: "allow-list"; rules: [{ domain: "pypi.org" }] };
      }>().toExtend<SandboxCreateInput>();
      expectTypeOf<{ networkPolicy: { type: "deny-all" } }>().toExtend<SandboxCreateInput>();
      expectTypeOf<{ networkPolicy: { type: "allow-list" } }>().not.toExtend<SandboxCreateInput>();
      expectTypeOf<{
        networkPolicy: { type: "deny-all"; rules: [{ domain: "pypi.org" }] };
      }>().not.toExtend<SandboxCreateInput>();
    });

    it("sends allow-list rules in the network policy", async () => {
      const apiClient = {
        POST: vi.fn().mockResolvedValue({
          data: { id: "sbx-123" },
          error: undefined,
          response: new Response(null, { status: 201 }),
        }),
      } as unknown as Client<paths>;
      const client = new SandboxesClient(apiClient, "tea-default");

      await client.create({
        networkPolicy: {
          type: "allow-list",
          rules: [{ domain: "pypi.org" }, { domain: "*.github.com", protocol: "https" }],
        },
      });
      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: {
          ownerId: "tea-default",
          networkPolicy: {
            type: "allow-list",
            rules: [{ domain: "pypi.org" }, { domain: "*.github.com", protocol: "https" }],
          },
        },
      });
    });

    it("passes caller-supplied options", async () => {
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
          plan: "4c-8g",
          timeoutSeconds: 600,
          idleTimeoutSeconds: 0,
          networkPolicy: { type: "deny-all" },
          env: { NODE_ENV: "test" },
        }),
      ).resolves.toEqual(sandbox);
      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: {
          ownerId: "tea-default",
          plan: "4c-8g",
          timeoutSeconds: 600,
          idleTimeoutSeconds: 0,
          networkPolicy: { type: "deny-all" },
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

    it("forwards the snapshot name", async () => {
      const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
      const client = new SandboxesClient(apiClient);

      await client.create({ ownerId: "tea-test", snapshotName: "gold" });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test", snapshotName: "gold" },
      });
    });

    it("sends an image ID as the build ID", async () => {
      const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
      const client = new SandboxesClient(apiClient);

      await client.create({ ownerId: "tea-test", image: IMAGE.id });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test", buildId: IMAGE.id },
      });
    });

    it("sends an image name as the build name", async () => {
      const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
      const client = new SandboxesClient(apiClient);

      await client.create({ ownerId: "tea-test", image: "agent-runtime" });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test", buildName: "agent-runtime" },
      });
    });

    it.each(["sbb-runtime", "sbb-abc", `${IMAGE.id}x`])(
      "sends %s, which is not in the image ID format, as a name",
      async (image) => {
        const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
        const client = new SandboxesClient(apiClient);

        await client.create({ ownerId: "tea-test", image });

        expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
          body: { ownerId: "tea-test", buildName: image },
        });
      },
    );

    it("forwards an empty image as a name instead of dropping it", async () => {
      const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
      const client = new SandboxesClient(apiClient);

      await client.create({ ownerId: "tea-test", image: "" });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test", buildName: "" },
      });
    });

    it("forwards the deprecated build ID", async () => {
      const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
      const client = new SandboxesClient(apiClient);

      await client.create({ ownerId: "tea-test", buildId: IMAGE.id });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test", buildId: IMAGE.id },
      });
    });

    it("forwards an empty build ID instead of dropping it", async () => {
      const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
      const client = new SandboxesClient(apiClient);

      await client.create({ ownerId: "tea-test", buildId: "" });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test", buildId: "" },
      });
    });

    it("forwards the deprecated build name", async () => {
      const apiClient = mockApiClient("POST", { status: 201, data: { id: "sbx-123" } });
      const client = new SandboxesClient(apiClient);

      await client.create({ ownerId: "tea-test", buildName: "python" });

      expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes", {
        body: { ownerId: "tea-test", buildName: "python" },
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
        input: { snapshotName: "missing" },
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
        input: { snapshotName: "runtime", plan: "4c-8g" },
        ErrorClass: SandboxSnapshotPlanMismatchError,
      },
      {
        status: 400,
        code: "invalid_snapshot_name",
        input: { snapshotName: "" },
        ErrorClass: ClientError,
      },
      {
        status: 404,
        code: "build_not_found",
        input: { image: "sbb-missing" },
        ErrorClass: SandboxImageNotFoundError,
      },
      {
        status: 404,
        code: "build_not_found",
        input: { image: "missing" },
        ErrorClass: SandboxImageNotFoundError,
      },
      {
        status: 409,
        code: "build_not_succeeded",
        input: { image: "sbb-running" },
        ErrorClass: SandboxImageNotReadyError,
      },
      {
        status: 409,
        code: "build_not_succeeded",
        input: { image: "python" },
        ErrorClass: SandboxImageNotReadyError,
      },
      {
        status: 409,
        code: "build_not_succeeded",
        input: { buildName: "python" },
        ErrorClass: SandboxImageNotReadyError,
      },
      {
        status: 404,
        code: undefined,
        input: { image: "sbb-missing" },
        ErrorClass: ClientError,
      },
      {
        status: 409,
        code: undefined,
        input: { image: "python" },
        ErrorClass: ClientError,
      },
      {
        status: 409,
        code: "sandbox_group_suspended",
        input: { image: "python" },
        ErrorClass: ClientError,
      },
      {
        status: 400,
        code: undefined,
        input: { image: "" },
        ErrorClass: ClientError,
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
          message: "Failed to create sandbox in workspace tea-default: rejected",
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
        message: "Failed to create sandbox in workspace tea-default: Not Found",
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
        context: "Failed to list snapshots in workspace tea-default",
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
      it("exposes a nullable optional snapshot name", () => {
        expectTypeOf<SandboxSnapshot["name"]>().toEqualTypeOf<string | null | undefined>();
      });

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

      it("sends the snapshot name", async () => {
        const namedSnapshot = { ...SNAPSHOT, name: "gold" };
        const apiClient = mockApiClient("POST", { status: 202, data: namedSnapshot });
        const client = new SandboxesClient(apiClient, "tea-default");

        await expect(
          client.snapshots.create({ sandboxId: "sbx-123", name: "gold" }),
        ).resolves.toEqual(namedSnapshot);

        expect(apiClient.POST).toHaveBeenCalledWith("/sandboxes/{sandboxId}/snapshots", {
          params: { path: { sandboxId: "sbx-123" }, query: { ownerId: "tea-default" } },
          body: { name: "gold" },
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
        { status: 400, code: "invalid_snapshot_name", ErrorClass: ClientError },
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

  describe("images", () => {
    const IMAGE_PATH = "/sandbox-groups/{sandboxGroupId}/builds";
    const IMAGE_GET_PATH = "/sandbox-groups/{sandboxGroupId}/builds/{buildId}";
    const imageGetInput = { sandboxGroupId: "sbg-123", imageId: IMAGE.id };

    it("exposes nullable optional failure and finish fields", () => {
      expectTypeOf<SandboxImage["failureReason"]>().toEqualTypeOf<string | null | undefined>();
      expectTypeOf<SandboxImage["finishedAt"]>().toEqualTypeOf<string | null | undefined>();
      expectTypeOf<SandboxImage["status"]>().toEqualTypeOf<
        "pending" | "running" | "succeeded" | "failed"
      >();
    });

    describe("import", () => {
      it("starts an import and returns it without an owner query", async () => {
        const apiClient = mockApiClient("POST", { status: 201, data: IMAGE });
        const client = new SandboxesClient(apiClient, "tea-default");

        await expect(client.images.import(IMAGE_IMPORT_INPUT)).resolves.toEqual(IMAGE);
        expect(apiClient.POST).toHaveBeenCalledWith(IMAGE_PATH, {
          params: { path: { sandboxGroupId: "sbg-123" } },
          body: { name: "python", sourceImage: "python:3.13" },
        });
      });

      it("sends the registry credentials", async () => {
        const apiClient = mockApiClient("POST", { status: 201, data: IMAGE });
        const client = new SandboxesClient(apiClient, "tea-default");
        const registryCredentials = { username: "bot", password: "s3cret" };

        await client.images.import({
          sandboxGroupId: "sbg-123",
          name: "internal",
          source: "ghcr.io/acme/internal:1.0",
          registryCredentials,
        });

        expect(apiClient.POST).toHaveBeenCalledWith(IMAGE_PATH, {
          params: { path: { sandboxGroupId: "sbg-123" } },
          body: {
            name: "internal",
            sourceImage: "ghcr.io/acme/internal:1.0",
            registryCredential: registryCredentials,
          },
        });
      });

      it("accepts a name with the image ID prefix", async () => {
        const apiClient = mockApiClient("POST", { status: 201, data: IMAGE });
        const client = new SandboxesClient(apiClient, "tea-default");

        await client.images.import({ ...IMAGE_IMPORT_INPUT, name: "sbb-runtime" });

        expect(apiClient.POST).toHaveBeenCalledWith(
          "/sandbox-groups/{sandboxGroupId}/builds",
          expect.objectContaining({ body: expect.objectContaining({ name: "sbb-runtime" }) }),
        );
      });

      it("returns the existing image when the group already has the digest", async () => {
        const succeeded: SandboxImage = {
          ...IMAGE,
          status: "succeeded",
          finishedAt: "2026-10-01T00:00:10Z",
        };
        const apiClient = mockApiClient("POST", { status: 201, data: succeeded });
        const client = new SandboxesClient(apiClient, "tea-default");

        await expect(client.images.import(IMAGE_IMPORT_INPUT)).resolves.toEqual(succeeded);
      });

      const importErrorRows: {
        status: number;
        code: string | undefined;
        ErrorClass: typeof ClientError;
      }[] = [
        { status: 400, code: undefined, ErrorClass: ClientError },
        { status: 400, code: "invalid_sandbox_group_id", ErrorClass: ClientError },
        { status: 404, code: undefined, ErrorClass: ClientError },
        { status: 409, code: "sandbox_group_suspended", ErrorClass: ClientError },
        { status: 429, code: undefined, ErrorClass: ClientError },
      ];

      it.each(importErrorRows)(
        "maps $status with code $code to $ErrorClass.name",
        async ({ status, code, ErrorClass }) => {
          const apiClient = mockApiClient("POST", {
            status,
            error: { message: "rejected", code },
          });
          const client = new SandboxesClient(apiClient, "tea-default");

          const error = await client.images.import(IMAGE_IMPORT_INPUT).catch((err) => err);
          expect(error.constructor).toBe(ErrorClass);
          expect(error).toMatchObject({
            statusCode: status,
            code,
            message: "Failed to import image: rejected",
          });
        },
      );
    });

    describe("get", () => {
      it("retrieves an image by group and ID", async () => {
        const failed: SandboxImage = {
          ...IMAGE,
          status: "failed",
          failureReason: "image is not linux/amd64",
          finishedAt: "2026-10-01T00:00:10Z",
        };
        const apiClient = mockApiClient("GET", { status: 200, data: failed });
        const client = new SandboxesClient(apiClient, "tea-default");

        await expect(client.images.get(imageGetInput)).resolves.toEqual(failed);
        expect(apiClient.GET).toHaveBeenCalledWith(IMAGE_GET_PATH, {
          params: { path: { sandboxGroupId: "sbg-123", buildId: IMAGE.id } },
        });
      });

      it("throws SandboxImageNotFoundError for a missing or foreign image", async () => {
        const apiClient = mockApiClient("GET", {
          status: 404,
          error: { message: "not found: build", code: "build_not_found" },
        });
        const client = new SandboxesClient(apiClient, "tea-default");

        const error = await client.images.get(imageGetInput).catch((err) => err);
        expect(error.constructor).toBe(SandboxImageNotFoundError);
        expect(error).toMatchObject({
          statusCode: 404,
          code: "build_not_found",
          message: "Failed to get image: not found: build",
        });
      });

      it("keeps other errors as plain ClientError", async () => {
        const apiClient = mockApiClient("GET", {
          status: 400,
          error: { message: "invalid build ID" },
        });
        const client = new SandboxesClient(apiClient, "tea-default");

        const error = await client.images.get(imageGetInput).catch((err) => err);
        expect(error.constructor).toBe(ClientError);
        expect(error).toMatchObject({
          statusCode: 400,
          message: "Failed to get image: invalid build ID",
        });
      });
    });

    describe("deprecated builds", () => {
      it("keeps the build types and errors as aliases of the image ones", () => {
        expectTypeOf<SandboxBuild>().toEqualTypeOf<SandboxImage>();
        expect(SandboxBuildNotFoundError).toBe(SandboxImageNotFoundError);
        expect(SandboxBuildNotReadyError).toBe(SandboxImageNotReadyError);
      });

      it("builds.create imports the image", async () => {
        const apiClient = mockApiClient("POST", { status: 201, data: IMAGE });
        const client = new SandboxesClient(apiClient, "tea-default");
        const registryCredential = { username: "bot", password: "s3cret" };

        await expect(
          client.builds.create({
            sandboxGroupId: "sbg-123",
            name: "python",
            sourceImage: "python:3.13",
            registryCredential,
          }),
        ).resolves.toEqual(IMAGE);
        expect(apiClient.POST).toHaveBeenCalledWith(IMAGE_PATH, {
          params: { path: { sandboxGroupId: "sbg-123" } },
          body: { name: "python", sourceImage: "python:3.13", registryCredential },
        });
      });

      it("builds.create still sends a name starting with sbb-", async () => {
        const apiClient = mockApiClient("POST", { status: 201, data: IMAGE });
        const client = new SandboxesClient(apiClient, "tea-default");

        await client.builds.create({
          sandboxGroupId: "sbg-123",
          name: "sbb-runtime",
          sourceImage: "python:3.13",
        });

        expect(apiClient.POST).toHaveBeenCalledWith(IMAGE_PATH, {
          params: { path: { sandboxGroupId: "sbg-123" } },
          body: { name: "sbb-runtime", sourceImage: "python:3.13" },
        });
      });

      it("builds.get gets the image", async () => {
        const apiClient = mockApiClient("GET", { status: 200, data: IMAGE });
        const client = new SandboxesClient(apiClient, "tea-default");

        await expect(
          client.builds.get({ sandboxGroupId: "sbg-123", buildId: IMAGE.id }),
        ).resolves.toEqual(IMAGE);
        expect(apiClient.GET).toHaveBeenCalledWith(IMAGE_GET_PATH, {
          params: { path: { sandboxGroupId: "sbg-123", buildId: IMAGE.id } },
        });
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
        POST: vi.fn().mockResolvedValue({
          data: connection,
          error: undefined,
          response: new Response(null, { status: 200 }),
        }),
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

    describe.each([
      {
        name: "upload",
        call: (c: SandboxesClient, path: string) => c.upload("sbx-123", path, "hi", "tea-test"),
      },
      {
        name: "download",
        call: (c: SandboxesClient, path: string) => c.download("sbx-123", path, "tea-test"),
      },
    ])("$name path cleaning", ({ name, call }) => {
      it.each([
        ["/tmp/trailing-slash/", "/tmp/trailing-slash"],
        ["workspace/", "workspace"],
        ["/app/./data/../data.txt", "/app/data.txt"],
        ["/app//x", "/app/x"],
        ["//app/x", "/app/x"],
        ["./", "."],
        ["/", "/"],
      ])("sends %j as %j", async (path, cleaned) => {
        const apiClient = {
          POST: vi.fn().mockResolvedValue({
            data: CONNECT_RESPONSE,
            error: undefined,
            response: new Response(null, { status: 200 }),
          }),
        } as unknown as Client<paths>;
        vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(null));

        await call(new SandboxesClient(apiClient), path);

        expect(apiClient.POST).toHaveBeenCalledWith(
          "/sandboxes/{sandboxId}/files/{operation}/token",
          {
            params: {
              path: { sandboxId: "sbx-123", operation: name },
              query: { ownerId: "tea-test", path: cleaned },
            },
          },
        );
      });

      it("rejects an empty path without minting a token", async () => {
        const apiClient = { POST: vi.fn() } as unknown as Client<paths>;

        await expect(call(new SandboxesClient(apiClient), "")).rejects.toThrow("path is required");
        expect(apiClient.POST).not.toHaveBeenCalled();
      });
    });

    it("throws AbortError when reading an upload error response is aborted", async () => {
      const apiClient = {
        POST: vi.fn().mockResolvedValue({
          data: CONNECT_RESPONSE,
          error: undefined,
          response: new Response(null, { status: 200 }),
        }),
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
        POST: vi.fn().mockResolvedValue({
          data: connection,
          error: undefined,
          response: new Response(null, { status: 200 }),
        }),
      } as unknown as Client<paths>;
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response("hello", {
          headers: { "Content-Type": "application/octet-stream" },
        }),
      );
      const client = new SandboxesClient(apiClient);

      const downloaded = await client.download("sbx-123", "/app/hello.txt", "tea-test");
      expect(await new Blob([downloaded.data]).text()).toBe("hello");

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
        POST: vi.fn().mockResolvedValue({
          data: CONNECT_RESPONSE,
          error: undefined,
          response: new Response(null, { status: 200 }),
        }),
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

    describe("when the connect token request returns 404", () => {
      const mockTokenNotFound = (status: string): Client<paths> =>
        ({
          POST: vi.fn().mockResolvedValue({
            data: undefined,
            error: { message: "not found" },
            response: new Response(null, { status: 404 }),
          }),
          GET: vi.fn().mockResolvedValue({
            data: {
              id: "sbx-123",
              status,
              plan: "1c-2g",
              networkPolicy: { type: "deny-all" },
              region: "oregon",
              timeoutSeconds: 600,
              createdAt: "2026-10-16T09:02:00Z",
              terminatedAt: status === "terminated" ? "2026-10-16T09:12:00Z" : null,
            },
            error: undefined,
            response: new Response(null, { status: 200 }),
          }),
        }) as unknown as Client<paths>;

      // A pool sandbox that passed its timeout failed with "not found", and callers
      // retried it as if it were still starting.
      it.each([
        {
          name: "exec",
          call: (c: SandboxesClient) => collectOpenExec(c, "sbx-123", "echo hi", "tea-test"),
          context: "Failed to get connect token",
        },
        {
          name: "download",
          call: (c: SandboxesClient) => c.download("sbx-123", "/tmp/out", "tea-test"),
          context: "Failed to get file connect token",
        },
      ])("$name throws SandboxEndedError for a terminated sandbox", async ({ call, context }) => {
        const client = new SandboxesClient(mockTokenNotFound("terminated"));

        const error = await call(client).catch((err) => err);
        expect(error).toBeInstanceOf(SandboxEndedError);
        expect(error).toMatchObject({
          statusCode: 404,
          sandboxStatus: "terminated",
          message: `${context}: sandbox sbx-123 was terminated at 2026-10-16T09:12:00Z`,
        });
      });

      it("keeps the 404 for a sandbox that is still running", async () => {
        const client = new SandboxesClient(mockTokenNotFound("running"));

        const error = await collectOpenExec(client, "sbx-123", "echo hi", "tea-test").catch(
          (err) => err,
        );
        expect(error).not.toBeInstanceOf(SandboxEndedError);
        expect(error).toMatchObject({
          statusCode: 404,
          message: "Failed to get connect token: not found",
        });
      });
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

  describe("waiting", () => {
    beforeEach(() => {
      vi.useFakeTimers();
    });
    afterEach(() => {
      vi.useRealTimers();
    });

    const sandboxWithStatus = (status: string) => ({
      data: {
        id: "sbx-123",
        status,
        plan: "starter",
        networkPolicy: { type: "deny-all" },
        region: "oregon",
        timeoutSeconds: 600,
        createdAt: "2026-10-20T10:00:00Z",
        terminatedAt: null,
      },
      error: undefined,
      response: new Response(null, { status: 200 }),
    });
    const snapshotWithStatus = (status: string, error: string | null = null) => ({
      data: { ...SNAPSHOT, status, error },
      error: undefined,
      response: new Response(null, { status: 200 }),
    });

    describe.each([
      {
        name: "sandbox",
        wait: (
          client: SandboxesClient,
          options: Parameters<SandboxesClient["waitUntilRunning"]>[1],
        ) => client.waitUntilRunning("sbx-123", options),
        ready: sandboxWithStatus("running"),
        pending: sandboxWithStatus("creating"),
      },
      {
        name: "snapshot",
        wait: (
          client: SandboxesClient,
          options: Parameters<SandboxesClient["waitUntilRunning"]>[1],
        ) =>
          client.snapshots.waitUntilAvailable(
            { sandboxGroupId: "sbg-123", snapshotId: SNAPSHOT.id },
            options,
          ),
        ready: snapshotWithStatus("available"),
        pending: snapshotWithStatus("creating"),
      },
    ])("$name wait limits", ({ wait, ready, pending }) => {
      it("times out and aborts an in-flight request even if the request never settles", async () => {
        const GET = vi.fn().mockImplementation(() => new Promise<never>(() => {}));
        const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

        const waiting = wait(client, { timeoutMs: 100 });
        const assertion = expect(waiting).rejects.toBeInstanceOf(TimeoutError);
        const requestSignal = GET.mock.calls[0][1].signal as AbortSignal;
        expect(requestSignal.aborted).toBe(false);
        await vi.advanceTimersByTimeAsync(100);
        await assertion;
        await expect(waiting).rejects.toMatchObject({ timeoutMs: 100, lastStatus: undefined });
        expect(requestSignal.aborted).toBe(true);
        expect(vi.getTimerCount()).toBe(0);
      });

      it("cancels an in-flight request and ignores its late success", async () => {
        let resolveRequest: (value: typeof ready) => void = () => {};
        const GET = vi.fn().mockImplementation(
          () =>
            new Promise<typeof ready>((resolve) => {
              resolveRequest = resolve;
            }),
        );
        const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");
        const controller = new AbortController();

        const waiting = wait(client, { signal: controller.signal });
        const assertion = expect(waiting).rejects.toBeInstanceOf(AbortError);
        const requestSignal = GET.mock.calls[0][1].signal as AbortSignal;
        controller.abort();
        await assertion;
        expect(requestSignal.aborted).toBe(true);
        resolveRequest(ready);
        await vi.advanceTimersByTimeAsync(1000);
        expect(GET).toHaveBeenCalledTimes(1);
        expect(vi.getTimerCount()).toBe(0);
      });

      // Timing out here would tell create({ wait }) callers to terminate a resource that just
      // became ready.
      it("returns a ready response received after the deadline before the timer runs", async () => {
        const GET = vi.fn().mockImplementation(async () => {
          vi.setSystemTime(Date.now() + 101);
          return ready;
        });
        const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

        await expect(wait(client, { timeoutMs: 100 })).resolves.toMatchObject({
          status: ready.data.status,
        });
        expect(vi.getTimerCount()).toBe(0);
      });

      it("times out on a pending response received after the deadline", async () => {
        const GET = vi.fn().mockImplementation(async () => {
          vi.setSystemTime(Date.now() + 101);
          return pending;
        });
        const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

        await expect(wait(client, { timeoutMs: 100 })).rejects.toMatchObject({
          lastStatus: "creating",
        });
        expect(GET).toHaveBeenCalledTimes(1);
        expect(vi.getTimerCount()).toBe(0);
      });

      it("rejects success if the caller aborts during the request", async () => {
        const controller = new AbortController();
        const GET = vi.fn().mockImplementation(async () => {
          controller.abort();
          return ready;
        });
        const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

        await expect(wait(client, { signal: controller.signal })).rejects.toBeInstanceOf(
          AbortError,
        );
        expect(vi.getTimerCount()).toBe(0);
      });

      it("waits out a timeout shorter than the polling interval", async () => {
        const GET = vi.fn().mockResolvedValue(pending);
        const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");
        let settled = false;

        const waiting = wait(client, { timeoutMs: 100, intervalMs: 250 });
        const assertion = expect(waiting).rejects.toBeInstanceOf(TimeoutError);
        void waiting.catch(() => {
          settled = true;
        });
        await vi.advanceTimersByTimeAsync(99);
        expect(settled).toBe(false);
        await vi.advanceTimersByTimeAsync(1);
        await assertion;
        expect(GET).toHaveBeenCalledTimes(1);
        expect(vi.getTimerCount()).toBe(0);
      });

      it("cleans up the deadline timer and caller's abort listener after success", async () => {
        const GET = vi.fn().mockResolvedValue(ready);
        const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");
        const controller = new AbortController();
        const remove = vi.spyOn(controller.signal, "removeEventListener");

        await wait(client, { signal: controller.signal });
        expect(vi.getTimerCount()).toBe(0);
        expect(remove).toHaveBeenCalledWith("abort", expect.any(Function));
      });
    });

    it.each([
      { timeoutMs: -1 },
      { timeoutMs: Number.NaN },
      { timeoutMs: Number.POSITIVE_INFINITY },
      { timeoutMs: 2_147_483_648 },
      { intervalMs: 0 },
      { intervalMs: -1 },
      { intervalMs: Number.NaN },
      { intervalMs: Number.POSITIVE_INFINITY },
    ])("rejects invalid wait options %o without requesting", async (options) => {
      const GET = vi.fn();
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      await expect(client.waitUntilRunning("sbx-123", options)).rejects.toBeInstanceOf(RangeError);
      expect(GET).not.toHaveBeenCalled();
      expect(vi.getTimerCount()).toBe(0);
    });

    it("treats a zero timeout as an immediate deadline", async () => {
      const GET = vi.fn();
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      await expect(client.waitUntilRunning("sbx-123", { timeoutMs: 0 })).rejects.toBeInstanceOf(
        TimeoutError,
      );
      expect(GET).not.toHaveBeenCalled();
      expect(vi.getTimerCount()).toBe(0);
    });

    it("waitUntilRunning polls until the sandbox runs", async () => {
      const GET = vi
        .fn()
        .mockResolvedValueOnce(sandboxWithStatus("creating"))
        .mockResolvedValueOnce(sandboxWithStatus("creating"))
        .mockResolvedValueOnce(sandboxWithStatus("running"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      const waiting = client.waitUntilRunning("sbx-123");
      await vi.advanceTimersByTimeAsync(750);

      await expect(waiting).resolves.toMatchObject({ id: "sbx-123", status: "running" });
      expect(GET).toHaveBeenCalledTimes(3);
    });

    // Doubling from 250 ms keeps short waits fast while a slow one stays
    // under the API rate limit.
    it("doubles the polling interval up to 2 seconds", async () => {
      const GET = vi.fn().mockResolvedValue(sandboxWithStatus("creating"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      const waiting = client.waitUntilRunning("sbx-123", { timeoutMs: 10_000 });
      const assertion = expect(waiting).rejects.toBeInstanceOf(SandboxWaitTimeoutError);
      const callsAt = async (ms: number) => {
        await vi.advanceTimersByTimeAsync(ms - Date.now());
        return GET.mock.calls.length;
      };
      const start = Date.now();
      const counts = [];
      for (const ms of [0, 250, 750, 1750, 3750, 5750, 7750]) {
        counts.push(await callsAt(start + ms));
      }
      expect(counts).toEqual([1, 2, 3, 4, 5, 6, 7]);
      await vi.advanceTimersByTimeAsync(10_000);
      await assertion;
    });

    it("keeps a fixed interval longer than 2 seconds", async () => {
      const GET = vi.fn().mockResolvedValue(sandboxWithStatus("creating"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      const waiting = client.waitUntilRunning("sbx-123", { timeoutMs: 12_000, intervalMs: 5000 });
      const assertion = expect(waiting).rejects.toBeInstanceOf(SandboxWaitTimeoutError);
      await vi.advanceTimersByTimeAsync(10_000);
      expect(GET).toHaveBeenCalledTimes(3);
      await vi.advanceTimersByTimeAsync(2000);
      await assertion;
    });

    // A sandbox that errored or was suspended never becomes running, so
    // waiting out the timeout would only delay the failure.
    it("waitUntilRunning throws as soon as the sandbox can't run", async () => {
      const GET = vi.fn().mockResolvedValue(sandboxWithStatus("errored"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      const waiting = client.waitUntilRunning("sbx-123");
      await expect(waiting).rejects.toBeInstanceOf(SandboxNotRunningError);
      await expect(waiting).rejects.toMatchObject({
        message: "Sandbox sbx-123 is errored, not running",
        sandboxId: "sbx-123",
        sandboxStatus: "errored",
      });
      expect(GET).toHaveBeenCalledTimes(1);
    });

    it("waitUntilRunning throws TimeoutError after timeoutMs", async () => {
      const GET = vi.fn().mockResolvedValue(sandboxWithStatus("creating"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      const waiting = client.waitUntilRunning("sbx-123", { timeoutMs: 1000 });
      const assertion = expect(waiting).rejects.toBeInstanceOf(SandboxWaitTimeoutError);
      await vi.advanceTimersByTimeAsync(1000);
      await assertion;
      await expect(waiting).rejects.toMatchObject({
        sandboxId: "sbx-123",
        timeoutMs: 1000,
        lastStatus: "creating",
      });
    });

    // Matches the CLI's `sandboxes create --wait`.
    it.each([
      {
        name: "waitUntilRunning",
        wait: (client: SandboxesClient) => client.waitUntilRunning("sbx-123"),
      },
      {
        name: "create with wait",
        wait: (client: SandboxesClient) =>
          client.create({ wait: true }).catch((err: SandboxCreateWaitError) => {
            throw err.cause;
          }),
      },
    ])("$name times out after 60 seconds by default", async ({ wait }) => {
      const POST = vi.fn().mockResolvedValue({
        ...sandboxWithStatus("creating"),
        response: new Response(null, { status: 201 }),
      });
      const GET = vi.fn().mockResolvedValue(sandboxWithStatus("creating"));
      const client = new SandboxesClient({ POST, GET } as unknown as Client<paths>, "tea-default");
      let settled = false;

      const waiting = wait(client);
      const assertion = expect(waiting).rejects.toBeInstanceOf(SandboxWaitTimeoutError);
      void waiting.catch(() => {
        settled = true;
      });
      await vi.advanceTimersByTimeAsync(59_999);
      expect(settled).toBe(false);
      await vi.advanceTimersByTimeAsync(1);
      await assertion;
      await expect(waiting).rejects.toMatchObject({ sandboxId: "sbx-123", timeoutMs: 60_000 });
    });

    it("snapshots.waitUntilAvailable times out after 5 minutes by default", async () => {
      const GET = vi.fn().mockResolvedValue(snapshotWithStatus("creating"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");
      let settled = false;

      const waiting = client.snapshots.waitUntilAvailable({
        sandboxGroupId: "sbg-123",
        snapshotId: SNAPSHOT.id,
      });
      const assertion = expect(waiting).rejects.toBeInstanceOf(SandboxSnapshotWaitTimeoutError);
      void waiting.catch(() => {
        settled = true;
      });
      await vi.advanceTimersByTimeAsync(5 * 60_000 - 1);
      expect(settled).toBe(false);
      await vi.advanceTimersByTimeAsync(1);
      await assertion;
      await expect(waiting).rejects.toMatchObject({
        snapshotId: SNAPSHOT.id,
        timeoutMs: 5 * 60_000,
        lastStatus: "creating",
      });
    });

    const imageWithStatus = (status: string, failureReason: string | null = null) => ({
      data: { ...IMAGE, status, failureReason },
      error: undefined,
      response: new Response(null, { status: 200 }),
    });

    it("images.waitUntilReady polls until the image succeeds", async () => {
      const GET = vi
        .fn()
        .mockResolvedValueOnce(imageWithStatus("pending"))
        .mockResolvedValueOnce(imageWithStatus("running"))
        .mockResolvedValueOnce(imageWithStatus("succeeded"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      const waiting = client.images.waitUntilReady({
        sandboxGroupId: "sbg-123",
        imageId: IMAGE.id,
      });
      await vi.advanceTimersByTimeAsync(250 + 500);

      await expect(waiting).resolves.toMatchObject({ status: "succeeded" });
      expect(GET).toHaveBeenCalledTimes(3);
      expect(GET).toHaveBeenCalledWith(
        "/sandbox-groups/{sandboxGroupId}/builds/{buildId}",
        expect.objectContaining({
          params: { path: { sandboxGroupId: "sbg-123", buildId: IMAGE.id } },
        }),
      );
    });

    it("images.waitUntilReady throws with the reason when the import fails", async () => {
      const GET = vi.fn().mockResolvedValue(imageWithStatus("failed", "image is not linux/amd64"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      const waiting = client.images.waitUntilReady({
        sandboxGroupId: "sbg-123",
        imageId: IMAGE.id,
      });
      await expect(waiting).rejects.toBeInstanceOf(SandboxImageFailedError);
      await expect(waiting).rejects.toMatchObject({
        message: `Image ${IMAGE.id} failed to import: image is not linux/amd64`,
        imageId: IMAGE.id,
        failureReason: "image is not linux/amd64",
      });
    });

    it("images.waitUntilReady times out after 10 minutes by default", async () => {
      const GET = vi.fn().mockResolvedValue(imageWithStatus("running"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");
      let settled = false;

      const waiting = client.images.waitUntilReady({
        sandboxGroupId: "sbg-123",
        imageId: IMAGE.id,
      });
      const assertion = expect(waiting).rejects.toBeInstanceOf(SandboxImageWaitTimeoutError);
      void waiting.catch(() => {
        settled = true;
      });
      await vi.advanceTimersByTimeAsync(10 * 60_000 - 1);
      expect(settled).toBe(false);
      await vi.advanceTimersByTimeAsync(1);
      await assertion;
      await expect(waiting).rejects.toMatchObject({
        imageId: IMAGE.id,
        timeoutMs: 10 * 60_000,
        lastStatus: "running",
      });
    });

    it("waitUntilRunning stops when the signal aborts", async () => {
      const GET = vi.fn().mockResolvedValue(sandboxWithStatus("creating"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");
      const controller = new AbortController();

      const waiting = client.waitUntilRunning("sbx-123", { signal: controller.signal });
      const assertion = expect(waiting).rejects.toBeInstanceOf(AbortError);
      await vi.advanceTimersByTimeAsync(100);
      controller.abort();
      await assertion;
    });

    it("snapshots.waitUntilAvailable polls until the snapshot is available", async () => {
      const GET = vi
        .fn()
        .mockResolvedValueOnce(snapshotWithStatus("creating"))
        .mockResolvedValueOnce(snapshotWithStatus("available"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      const waiting = client.snapshots.waitUntilAvailable({
        sandboxGroupId: "sbg-123",
        snapshotId: SNAPSHOT.id,
      });
      await vi.advanceTimersByTimeAsync(250);

      await expect(waiting).resolves.toMatchObject({ status: "available" });
    });

    it("snapshots.waitUntilAvailable throws with the reason when capture fails", async () => {
      const GET = vi.fn().mockResolvedValue(snapshotWithStatus("failed", "capture timed out"));
      const client = new SandboxesClient({ GET } as unknown as Client<paths>, "tea-default");

      const waiting = client.snapshots.waitUntilAvailable({
        sandboxGroupId: "sbg-123",
        snapshotId: SNAPSHOT.id,
      });
      await expect(waiting).rejects.toBeInstanceOf(SandboxSnapshotFailedError);
      await expect(waiting).rejects.toMatchObject({
        message: `Snapshot ${SNAPSHOT.id} failed to capture: capture timed out`,
        snapshotId: SNAPSHOT.id,
        snapshotError: "capture timed out",
      });
    });

    describe("create with wait", () => {
      const clientWith = (createdStatus: string, ...polled: string[]) => {
        const POST = vi.fn().mockResolvedValue({
          ...sandboxWithStatus(createdStatus),
          response: new Response(null, { status: 201 }),
        });
        const GET = vi.fn();
        for (const status of polled) GET.mockResolvedValueOnce(sandboxWithStatus(status));
        const client = new SandboxesClient(
          { POST, GET } as unknown as Client<paths>,
          "tea-default",
        );
        return { client, POST, GET };
      };

      it("returns the created sandbox without polling when wait is unset", async () => {
        const { client, GET } = clientWith("creating");

        await expect(client.create()).resolves.toMatchObject({ status: "creating" });
        expect(GET).not.toHaveBeenCalled();
      });

      it("polls until running and keeps wait out of the request body", async () => {
        const { client, POST, GET } = clientWith("creating", "creating", "running");

        const waiting = client.create({ ownerId: "tea-test", wait: true });
        await vi.advanceTimersByTimeAsync(250);

        await expect(waiting).resolves.toMatchObject({ status: "running" });
        expect(POST).toHaveBeenCalledWith("/sandboxes", { body: { ownerId: "tea-test" } });
        expect(GET).toHaveBeenCalledTimes(2);
        expect(GET.mock.calls[0][1].params.query).toEqual({ ownerId: "tea-test" });
      });

      it("skips polling when the created sandbox is already running", async () => {
        const { client, GET } = clientWith("running");

        await expect(client.create({ wait: true })).resolves.toMatchObject({ status: "running" });
        expect(GET).not.toHaveBeenCalled();
      });

      it("throws without polling when the created sandbox errored", async () => {
        const { client, GET } = clientWith("errored");

        const error = await client.create({ wait: true }).catch((err) => err);
        expect(error).toBeInstanceOf(SandboxCreateWaitError);
        expect(error).toMatchObject({
          message:
            "Created sandbox sbx-123, but it is not running: Sandbox sbx-123 is errored, not running",
          sandboxId: "sbx-123",
        });
        expect(error.cause).toBeInstanceOf(SandboxNotRunningError);
        expect(GET).not.toHaveBeenCalled();
      });

      // No sandbox exists yet, so these throw plainly rather than as SandboxCreateWaitError.
      it.each([
        { timeoutMs: -1 },
        { timeoutMs: Number.NaN },
        { timeoutMs: 2_147_483_648 },
        { intervalMs: 0 },
        { intervalMs: Number.POSITIVE_INFINITY },
      ])("rejects wait options %o without creating a sandbox", async (wait) => {
        const { client, POST } = clientWith("creating");

        await expect(client.create({ wait })).rejects.toThrow(RangeError);
        expect(POST).not.toHaveBeenCalled();
      });

      // The running-response shortcut used to skip the check.
      it("rejects bad wait options even when the sandbox would come back running", async () => {
        const { client, POST } = clientWith("running");

        await expect(client.create({ wait: { intervalMs: 0 } })).rejects.toThrow(RangeError);
        expect(POST).not.toHaveBeenCalled();
      });

      it("throws AbortError without creating a sandbox when the signal already aborted", async () => {
        const { client, POST } = clientWith("creating");
        const controller = new AbortController();
        controller.abort();

        const error = await client.create({ wait: { signal: controller.signal } }).catch((e) => e);
        expect(error).toBeInstanceOf(AbortError);
        expect(error).not.toBeInstanceOf(SandboxCreateWaitError);
        expect(POST).not.toHaveBeenCalled();
      });

      it("returns a sandbox that runs just past the deadline", async () => {
        const { client, GET } = clientWith("creating");
        GET.mockImplementation(async () => {
          vi.setSystemTime(Date.now() + 1001);
          return sandboxWithStatus("running");
        });

        await expect(client.create({ wait: { timeoutMs: 1000 } })).resolves.toMatchObject({
          status: "running",
        });
      });

      it("passes wait options through", async () => {
        const { client, GET } = clientWith("creating");
        GET.mockResolvedValue(sandboxWithStatus("creating"));

        const waiting = client.create({ wait: { timeoutMs: 1000 } }).catch((err) => err);
        await vi.advanceTimersByTimeAsync(1000);
        const error = await waiting;
        expect(error).toBeInstanceOf(SandboxCreateWaitError);
        expect(error.cause).toBeInstanceOf(SandboxWaitTimeoutError);
        expect(error.cause).toMatchObject({ sandboxId: "sbx-123", timeoutMs: 1000 });
      });

      // Without the ID, the caller can't terminate a sandbox it is billed for.
      it.each([
        {
          name: "the caller aborts",
          poll: (GET: ReturnType<typeof vi.fn>) =>
            GET.mockResolvedValue(sandboxWithStatus("creating")),
          abort: true,
          cause: AbortError,
        },
        {
          name: "a status check gets a 5xx",
          poll: (GET: ReturnType<typeof vi.fn>) =>
            GET.mockResolvedValue({
              data: undefined,
              error: { message: "unavailable" },
              response: new Response(null, { status: 503 }),
            }),
          abort: false,
          cause: ServerError,
        },
        {
          name: "a status check gets a 4xx",
          poll: (GET: ReturnType<typeof vi.fn>) =>
            GET.mockResolvedValue({
              data: undefined,
              error: { message: "forbidden" },
              response: new Response(null, { status: 403 }),
            }),
          abort: false,
          cause: ClientError,
        },
        {
          name: "the fetch fails",
          poll: (GET: ReturnType<typeof vi.fn>) =>
            GET.mockRejectedValue(new TypeError("fetch failed")),
          abort: false,
          cause: TypeError,
        },
        {
          name: "a response body doesn't parse",
          poll: (GET: ReturnType<typeof vi.fn>) =>
            GET.mockRejectedValue(new SyntaxError("Unexpected end of JSON input")),
          abort: false,
          cause: SyntaxError,
        },
      ])("gives the sandbox ID when $name", async ({ poll, abort, cause }) => {
        const { client, GET } = clientWith("creating");
        poll(GET);
        const controller = new AbortController();

        const waiting = client.create({ wait: { signal: controller.signal } }).catch((err) => err);
        await vi.advanceTimersByTimeAsync(0);
        if (abort) controller.abort();
        const error = await waiting;

        expect(error).toBeInstanceOf(SandboxCreateWaitError);
        expect(error.sandboxId).toBe("sbx-123");
        expect(error.cause).toBeInstanceOf(cause);
        expect(vi.getTimerCount()).toBe(0);
      });
    });

    describe("snapshots.create with wait", () => {
      const clientWith = (created: ReturnType<typeof snapshotWithStatus>, ...polled: string[]) => {
        const POST = vi.fn().mockResolvedValue({
          ...created,
          response: new Response(null, { status: 202 }),
        });
        const GET = vi.fn();
        for (const status of polled) GET.mockResolvedValueOnce(snapshotWithStatus(status));
        const client = new SandboxesClient(
          { POST, GET } as unknown as Client<paths>,
          "tea-default",
        );
        return { client, POST, GET };
      };

      it("returns the created snapshot without polling when wait is unset", async () => {
        const { client, GET } = clientWith(snapshotWithStatus("creating"));

        await expect(client.snapshots.create({ sandboxId: "sbx-123" })).resolves.toMatchObject({
          status: "creating",
        });
        expect(GET).not.toHaveBeenCalled();
      });

      it("polls the new snapshot until available and keeps wait out of the request", async () => {
        const { client, POST, GET } = clientWith(
          snapshotWithStatus("creating"),
          "creating",
          "available",
        );

        const waiting = client.snapshots.create({
          sandboxId: "sbx-123",
          ownerId: "tea-test",
          wait: true,
        });
        await vi.advanceTimersByTimeAsync(250);

        await expect(waiting).resolves.toMatchObject({ status: "available" });
        expect(POST.mock.calls[0][1]).not.toHaveProperty("body");
        expect(GET).toHaveBeenCalledTimes(2);
        expect(GET.mock.calls[0][0]).toBe(
          "/sandbox-groups/{sandboxGroupId}/snapshots/{snapshotId}",
        );
        expect(GET.mock.calls[0][1].params).toEqual({
          path: { sandboxGroupId: "sbg-123", snapshotId: SNAPSHOT.id },
          query: { ownerId: "tea-test" },
        });
      });

      it("skips polling when the created snapshot is already available", async () => {
        const { client, GET } = clientWith(snapshotWithStatus("available"));

        await expect(
          client.snapshots.create({ sandboxId: "sbx-123", wait: true }),
        ).resolves.toMatchObject({ status: "available" });
        expect(GET).not.toHaveBeenCalled();
      });

      // Matches the CLI's `sandboxes snapshots create --wait`.
      it("times out after 5 minutes by default", async () => {
        const { client, GET } = clientWith(snapshotWithStatus("creating"));
        GET.mockResolvedValue(snapshotWithStatus("creating"));

        const waiting = client.snapshots
          .create({ sandboxId: "sbx-123", wait: true })
          .catch((err) => err);
        await vi.advanceTimersByTimeAsync(5 * 60_000);
        const error = await waiting;

        expect(error).toBeInstanceOf(SandboxSnapshotCreateWaitError);
        expect(error.cause).toBeInstanceOf(SandboxSnapshotWaitTimeoutError);
        expect(error.cause).toMatchObject({ timeoutMs: 5 * 60_000, lastStatus: "creating" });
      });

      it("gives both IDs when the capture fails", async () => {
        const { client, GET } = clientWith(snapshotWithStatus("failed", "capture timed out"));

        const error = await client.snapshots
          .create({ sandboxId: "sbx-123", wait: true })
          .catch((err) => err);

        expect(error).toBeInstanceOf(SandboxSnapshotCreateWaitError);
        expect(error).toMatchObject({
          message: `Created snapshot ${SNAPSHOT.id}, but it is not available: Snapshot ${SNAPSHOT.id} failed to capture: capture timed out`,
          snapshotId: SNAPSHOT.id,
          sandboxGroupId: "sbg-123",
        });
        expect(error.cause).toBeInstanceOf(SandboxSnapshotFailedError);
        expect(GET).not.toHaveBeenCalled();
      });

      // Without the IDs, the caller can't delete a snapshot it didn't want.
      it.each([
        { name: "the caller aborts", abort: true, poll: undefined, cause: AbortError },
        {
          name: "a status check gets a 5xx",
          abort: false,
          poll: {
            data: undefined,
            error: { message: "unavailable" },
            response: new Response(null, { status: 503 }),
          },
          cause: ServerError,
        },
        {
          name: "the fetch fails",
          abort: false,
          poll: new TypeError("fetch failed"),
          cause: TypeError,
        },
      ])("gives both IDs when $name", async ({ abort, poll, cause }) => {
        const { client, GET } = clientWith(snapshotWithStatus("creating"));
        if (poll instanceof Error) GET.mockRejectedValue(poll);
        else GET.mockResolvedValue(poll ?? snapshotWithStatus("creating"));
        const controller = new AbortController();

        const waiting = client.snapshots
          .create({ sandboxId: "sbx-123", wait: { signal: controller.signal } })
          .catch((err) => err);
        await vi.advanceTimersByTimeAsync(0);
        if (abort) controller.abort();
        const error = await waiting;

        expect(error).toBeInstanceOf(SandboxSnapshotCreateWaitError);
        expect(error).toMatchObject({ snapshotId: SNAPSHOT.id, sandboxGroupId: "sbg-123" });
        expect(error.cause).toBeInstanceOf(cause);
        expect(vi.getTimerCount()).toBe(0);
      });

      // No snapshot exists yet, so these throw plainly.
      it.each([
        { wait: { timeoutMs: -1 }, error: RangeError },
        { wait: { intervalMs: 0 }, error: RangeError },
        { wait: { signal: AbortSignal.abort() }, error: AbortError },
      ])("rejects $wait without creating a snapshot", async ({ wait, error }) => {
        const { client, POST } = clientWith(snapshotWithStatus("available"));

        await expect(client.snapshots.create({ sandboxId: "sbx-123", wait })).rejects.toThrow(
          error,
        );
        expect(POST).not.toHaveBeenCalled();
      });
    });
  });
});

describe("sandbox group selection", () => {
  it("passes group selection on create and preserves the returned group", async () => {
    const result = { id: "sbx-123", sandboxGroupId: "sbg-other" };
    const api = mockApiClient("POST", { status: 201, data: result });
    const client = new SandboxesClient(api, "tea-default");
    expect(await client.create({ sandboxGroupId: "sbg-other" })).toEqual(result);
    expect(api.POST).toHaveBeenCalledWith("/sandboxes", {
      body: { ownerId: "tea-default", sandboxGroupId: "sbg-other" },
    });
  });

  it("filters sandboxes and pages groups independently", async () => {
    const api = mockApiClient("GET", { status: 200, data: [] });
    const client = new SandboxesClient(api, "tea-default");
    await client.list({ sandboxGroupId: "sbg-other", cursor: "c1", limit: 5 });
    expect(api.GET).toHaveBeenLastCalledWith("/sandboxes", {
      params: {
        query: expect.objectContaining({ sandboxGroupId: "sbg-other", cursor: "c1", limit: 5 }),
      },
    });
    await client.listGroups({ cursor: "g1", limit: 2 });
    expect(api.GET).toHaveBeenLastCalledWith("/sandbox-groups", {
      params: { query: { ownerId: "tea-default", cursor: "g1", limit: 2 } },
    });
  });

  it("creates, retrieves, and updates groups with the effective limit returned by the API", async () => {
    const group = { id: "sbg-1", concurrencyLimit: 100 };
    const post = mockApiClient("POST", { status: 201, data: group });
    await expect(
      new SandboxesClient(post, "tea-default").createGroup({ name: "agents" }),
    ).resolves.toEqual(group);
    expect(post.POST).toHaveBeenCalledWith("/sandbox-groups", {
      body: { ownerId: "tea-default", name: "agents", region: "oregon" },
    });
    const get = mockApiClient("GET", { status: 200, data: group });
    await expect(new SandboxesClient(get).getGroup("sbg-1")).resolves.toEqual(group);
    const patch = mockApiClient("PATCH", { status: 200, data: group });
    await expect(new SandboxesClient(patch).updateGroup("sbg-1", 200)).resolves.toEqual(group);
    expect(patch.PATCH).toHaveBeenCalledWith("/sandbox-groups/{sandboxGroupId}", {
      params: { path: { sandboxGroupId: "sbg-1" } },
      body: { concurrencyLimit: 200 },
    });
  });
});
