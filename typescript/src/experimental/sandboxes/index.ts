import { posix } from "node:path";
import type { Readable } from "node:stream";
import type { Client } from "openapi-fetch";

import {
  AbortError,
  ClientError,
  RenderError,
  SandboxCreateWaitError,
  SandboxEndedError,
  SandboxNotRunningError,
  SandboxSnapshotCreateWaitError,
  SandboxSnapshotFailedError,
  SandboxSnapshotNotFoundError,
  SandboxSnapshotWaitTimeoutError,
  SandboxWaitTimeoutError,
} from "../../errors.js";
import type { components, paths } from "../../generated/schema.js";

import { getApiError } from "../../utils/http.js";
import { pollUntil, validateOptions } from "../../utils/poll-until.js";
import { getUserAgent } from "../../version.js";
import type { SandboxPlan } from "./types.js";

export type { SandboxPlan } from "./types.js";

const LEADING_SPACE = /^ /;
const TRAILING_CARRIAGE_RETURN = /\r$/;

type SandboxExecOutputEvent = {
  stream: "stdout" | "stderr";
  data: string;
};

type SandboxExecExitEvent = {
  exit_code: number;
};

type SandboxExecErrorEvent = {
  status: number;
  message: string;
};

type SandboxConnectOperation =
  paths["/sandboxes/{sandboxId}/runs/{operation}/token"]["post"]["parameters"]["path"]["operation"];

type SandboxFileOperation =
  paths["/sandboxes/{sandboxId}/files/{operation}/token"]["post"]["parameters"]["path"]["operation"];

export type SandboxUploadData = Buffer | Uint8Array | string | Readable;

export type SandboxUploadContentType =
  | "application/octet-stream"
  | "application/x-tar"
  | "application/gzip";

export type SandboxUploadOptions = {
  contentType?: SandboxUploadContentType;
  signal?: AbortSignal;
};

export type SandboxDownload = {
  /** Backed by an `ArrayBuffer`, so it passes to Web and Bun APIs that take `Uint8Array<ArrayBuffer>`. */
  data: ReturnType<typeof Buffer.from>;
  size: number;
  contentType?: string;
};

export type SandboxExecEvent =
  | ({ type: "output" } & SandboxExecOutputEvent)
  | ({ type: "exit" } & SandboxExecExitEvent);

type SandboxSourceInput =
  | {
      /**
       * Start from this snapshot instead of the base image. Must be `available` and in the same
       * sandbox group. For a `runtime` snapshot, `plan` must match the snapshot's plan.
       */
      snapshotId?: string;
      snapshotName?: never;
      buildId?: never;
      buildName?: never;
    }
  | {
      snapshotId?: never;
      /**
       * Start from the available snapshot this name currently resolves to in the sandbox group.
       * For a `runtime` snapshot, `plan` must match the snapshot's plan.
       */
      snapshotName?: string;
      buildId?: never;
      buildName?: never;
    }
  | {
      snapshotId?: never;
      snapshotName?: never;
      /**
       * Start from this build's image instead of the base image. The build must have `succeeded`
       * and be in the same sandbox group.
       */
      buildId?: string;
      buildName?: never;
    }
  | {
      snapshotId?: never;
      snapshotName?: never;
      buildId?: never;
      /** Start from the newest `succeeded` build with this name in the sandbox group. */
      buildName?: string;
    };

/** A destination a sandbox under an `allow-list` network policy may reach. */
export type SandboxEgressRule = {
  /**
   * Hostname to admit. Matching is exact: `foo.local` does not cover `api.foo.local`, which
   * needs its own rule or `*.foo.local`. A wildcard is only allowed as the leftmost label.
   */
  domain: string;
  /** The API defaults to `https`. */
  protocol?: components["schemas"]["sandboxEgressRule"]["protocol"];
};

/**
 * How a sandbox's outbound traffic is handled. `allow-list` admits only the destinations in
 * `rules`; the other policy types take no rules.
 */
export type SandboxNetworkPolicy =
  | { type: "allow-all" | "deny-all"; rules?: never }
  | { type: "allow-list"; rules: SandboxEgressRule[] };

/** Options for creating a sandbox. Unset fields fall back to the API's defaults. */
export type SandboxCreateInput = SandboxSourceInput & {
  ownerId?: `tea-${string}`;
  plan?: SandboxPlan | (string & {});
  /** Maximum sandbox lifetime in seconds. The API defaults to 86400 (24 hours). */
  timeoutSeconds?: number;
  /**
   * Seconds of inactivity before the sandbox is suspended. Use 0 to disable automatic idle
   * suspension; positive values must be at least 300. The API defaults to 900.
   */
  idleTimeoutSeconds?: number;
  /** Defaults to the client's region, then to the workspace default. */
  region?: string;
  /** The API defaults to `allow-all`. */
  networkPolicy?: SandboxNetworkPolicy;
  /** Environment variables injected into the sandbox at creation. */
  env?: Record<string, string>;
  /**
   * Resolve only once the sandbox is `running`, as `waitUntilRunning` does. `true` uses the
   * default wait options. Bad options throw `RangeError`, and an already-aborted signal throws
   * `AbortError`, before the create request, so neither creates a sandbox. The wait starts after
   * the create request returns. If the wait fails, `create()` throws `SandboxCreateWaitError` with
   * the new sandbox's ID, so you can terminate it.
   */
  wait?: boolean | SandboxWaitOptions;
};

export type Sandbox = components["schemas"]["sandbox"];

/** Options for `waitUntilRunning` and `snapshots.waitUntilAvailable`. */
export type SandboxWaitOptions = {
  /**
   * Overall timeout, including requests. Defaults to 60 seconds for a sandbox, 5 minutes for a
   * snapshot.
   */
  timeoutMs?: number;
  /**
   * The first delay between status checks. It doubles after each check, up to 2 seconds or
   * `intervalMs`, whichever is longer. @default 250
   */
  intervalMs?: number;
  signal?: AbortSignal;
};

/** A sandbox snapshot as returned by the API. */
export type SandboxSnapshot = components["schemas"]["sandboxSnapshot"];

/** A snapshot paired with its pagination cursor. */
export type SandboxSnapshotWithCursor = components["schemas"]["sandboxSnapshotWithCursor"];

/**
 * `filesystem` captures the writable filesystem and restores onto any plan. `runtime` also
 * captures memory and CPU state and restores only onto the source sandbox's plan.
 */
export type SandboxSnapshotKind = components["schemas"]["sandboxSnapshotKind"];

/** `creating` until the capture finishes, then `available` or `failed`. */
export type SandboxSnapshotStatus = components["schemas"]["sandboxSnapshotStatus"];

/** Options for capturing a snapshot of a running sandbox. */
export type SandboxSnapshotCreateInput = {
  sandboxId: string;
  /** The API defaults to `runtime`. */
  kind?: SandboxSnapshotKind;
  /** Case-sensitive name for this snapshot. May be reused within the sandbox group. */
  name?: string;
  /** ISO 8601. Omit for Render's default snapshot lifetime. */
  expiresAt?: string;
  /** Defaults to the client's owner ID. */
  ownerId?: `tea-${string}`;
  /**
   * Resolve only once the snapshot is `available`, as `waitUntilAvailable` does. `true` uses the
   * default wait options. Bad options throw `RangeError`, and an already-aborted signal throws
   * `AbortError`, before the create request, so neither creates a snapshot. If the wait fails,
   * `create()` throws `SandboxSnapshotCreateWaitError` with the new snapshot's IDs.
   */
  wait?: boolean | SandboxWaitOptions;
};

/** Options for retrieving a snapshot. */
export type SandboxSnapshotGetInput = {
  sandboxGroupId: string;
  snapshotId: string;
  /** Defaults to the client's owner ID. */
  ownerId?: `tea-${string}`;
};

/** Options for listing the snapshots in a sandbox group, newest first. */
export type SandboxSnapshotListInput = {
  sandboxGroupId: string;
  status?: SandboxSnapshotStatus[];
  cursor?: string;
  /** 1 to 100. */
  limit?: number;
  /** Defaults to the client's owner ID. */
  ownerId?: `tea-${string}`;
};

/** Options for deleting a snapshot. Deleting is idempotent and leaves restored sandboxes intact. */
export type SandboxSnapshotDeleteInput = {
  sandboxGroupId: string;
  snapshotId: string;
  /** Defaults to the client's owner ID. */
  ownerId?: `tea-${string}`;
};

/** A sandbox build as returned by the API. */
export type SandboxBuild = components["schemas"]["sandboxBuild"];

/** `pending` or `running` until the conversion finishes, then `succeeded` or `failed`. */
export type SandboxBuildStatus = components["schemas"]["sandboxBuildStatus"];

/** The image a build converts, as the registry resolved it. */
export type SandboxBuildSource = SandboxBuild["source"];

/** Pulls `sourceImage` from a private registry. Used for that build only and never stored. */
export type SandboxRegistryCredential = NonNullable<
  components["schemas"]["sandboxBuildPOST"]["registryCredential"]
>;

/** Options for converting an image into a sandbox base image. */
export type SandboxBuildCreateInput = {
  sandboxGroupId: string;
  /** Names the image. Every build of an image shares it. 1 to 255 characters. */
  name: string;
  /** The image to convert, by tag or digest, like `python:3.13`. Must be linux/amd64. */
  sourceImage: string;
  registryCredential?: SandboxRegistryCredential;
};

/** Options for retrieving a build. */
export type SandboxBuildGetInput = {
  sandboxGroupId: string;
  buildId: string;
};

/** A sandbox group as returned by the API. */
export type SandboxGroup = components["schemas"]["sandboxGroup"];

/** A sandbox group paired with its pagination cursor. */
export type SandboxGroupWithCursor = components["schemas"]["sandboxGroupWithCursor"];

/** Options for listing sandbox groups. */
export type SandboxGroupListInput = {
  /** Defaults to the client's owner ID. */
  ownerId?: `tea-${string}`;
};

export class SandboxExecStreamError extends RenderError {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "SandboxExecStreamError";
    Object.setPrototypeOf(this, SandboxExecStreamError.prototype);
  }
}

function resolveOwnerId(
  ownerId: `tea-${string}` | undefined,
  defaultOwnerId: string | undefined,
): `tea-${string}` {
  const resolved = ownerId || defaultOwnerId;
  if (!resolved) {
    throw new RenderError(
      "ownerId is required. Provide it as a parameter or set the RENDER_WORKSPACE_ID environment variable.",
    );
  }
  return resolved as `tea-${string}`;
}

/**
 * Names the workspace in errors from calls scoped to one. A wrong workspace
 * (e.g. RENDER_WORKSPACE_ID left over in the shell) otherwise shows only as
 * "not found".
 */
function inWorkspace(context: string, ownerId: string): string {
  return `${context} in workspace ${ownerId}`;
}

/** Cleans a sandbox file path the way the API requires. */
function cleanSandboxPath(path: string): string {
  if (!path) {
    throw new RenderError("path is required");
  }
  const cleaned = posix.normalize(path);
  return cleaned.length > 1 && cleaned.endsWith("/") ? cleaned.slice(0, -1) : cleaned;
}

function optionalOwnerIdQuery(
  ownerId: `tea-${string}` | undefined,
  defaultOwnerId: string | undefined,
): { query: { ownerId: string } } | Record<string, never> {
  const resolved = ownerId || defaultOwnerId;
  return resolved ? { query: { ownerId: resolved } } : {};
}

const DEFAULT_WAIT_INTERVAL_MS = 250;
const DEFAULT_SANDBOX_WAIT_TIMEOUT_MS = 60_000;
const DEFAULT_SNAPSHOT_WAIT_TIMEOUT_MS = 5 * 60_000;

/**
 * Returns the sandbox if it is `running`, or `undefined` if it may still become `running`.
 * Throws `SandboxNotRunningError` if it can't.
 */
function runningSandbox(sandbox: Sandbox): Sandbox | undefined {
  switch (sandbox.status) {
    case "running":
      return sandbox;
    case "creating":
    case "resuming":
      return undefined;
    default:
      throw new SandboxNotRunningError(
        `Sandbox ${sandbox.id} is ${sandbox.status}, not running`,
        sandbox.id,
        sandbox.status,
      );
  }
}

/**
 * Returns the snapshot if it is `available`, or `undefined` if it is still capturing.
 * Throws `SandboxSnapshotFailedError` if the capture failed.
 */
function availableSnapshot(snapshot: SandboxSnapshot): SandboxSnapshot | undefined {
  if (snapshot.status === "available") return snapshot;
  if (snapshot.status === "failed") {
    throw new SandboxSnapshotFailedError(
      `Snapshot ${snapshot.id} failed to capture${snapshot.error ? `: ${snapshot.error}` : ""}`,
      snapshot.id,
      snapshot.error ?? undefined,
    );
  }
  return undefined;
}

/**
 * Fills in the defaults for a `create({ wait })` and checks them before the create request, so
 * bad options or an early abort create nothing. Returns `undefined` when not waiting.
 */
function resolveCreateWait(
  wait: boolean | SandboxWaitOptions | undefined,
  defaultTimeoutMs: number,
): (SandboxWaitOptions & { timeoutMs: number; intervalMs: number }) | undefined {
  const options = wait === true ? {} : wait || undefined;
  if (!options) return undefined;
  const resolved = {
    ...options,
    timeoutMs: options.timeoutMs ?? defaultTimeoutMs,
    intervalMs: options.intervalMs ?? DEFAULT_WAIT_INTERVAL_MS,
  };
  validateOptions(resolved);
  if (resolved.signal?.aborted) {
    throw new AbortError();
  }
  return resolved;
}

export class SandboxSnapshotsClient {
  constructor(
    private readonly apiClient: Client<paths>,
    private readonly defaultOwnerId?: string,
  ) {}

  async create({
    sandboxId,
    kind,
    name,
    expiresAt,
    ownerId,
    wait: waitInput,
  }: SandboxSnapshotCreateInput): Promise<SandboxSnapshot> {
    const wait = resolveCreateWait(waitInput, DEFAULT_SNAPSHOT_WAIT_TIMEOUT_MS);
    const body = {
      ...(kind ? { kind } : {}),
      ...(name === undefined ? {} : { name }),
      ...(expiresAt ? { expiresAt } : {}),
    } as components["schemas"]["sandboxSnapshotPOST"];
    const snapshot = unwrap(
      await this.apiClient.POST("/sandboxes/{sandboxId}/snapshots", {
        params: {
          path: { sandboxId },
          ...optionalOwnerIdQuery(ownerId, this.defaultOwnerId),
        },
        ...(kind || name !== undefined || expiresAt ? { body } : {}),
      }),
      "Failed to create snapshot",
    );
    if (!wait) {
      return snapshot;
    }
    // The snapshot exists from here on, so every failure must give the caller its IDs.
    try {
      return (
        availableSnapshot(snapshot) ??
        (await this.waitUntilAvailable(
          { sandboxGroupId: snapshot.sandboxGroupId, snapshotId: snapshot.id, ownerId },
          wait,
        ))
      );
    } catch (err) {
      const reason = err instanceof Error ? err.message : String(err);
      throw new SandboxSnapshotCreateWaitError(
        `Created snapshot ${snapshot.id}, but it is not available: ${reason}`,
        snapshot.id,
        snapshot.sandboxGroupId,
        err,
      );
    }
  }

  async get(
    { sandboxGroupId, snapshotId, ownerId }: SandboxSnapshotGetInput,
    signal?: AbortSignal,
  ): Promise<SandboxSnapshot> {
    return unwrap(
      await this.apiClient.GET("/sandbox-groups/{sandboxGroupId}/snapshots/{snapshotId}", {
        params: {
          path: { sandboxGroupId, snapshotId },
          ...optionalOwnerIdQuery(ownerId, this.defaultOwnerId),
        },
        ...(signal ? { signal } : {}),
      }),
      "Failed to get snapshot",
      getSnapshotApiError,
    );
  }

  /**
   * Waits until the snapshot is `available`, so new sandboxes can start from it. Throws
   * `SandboxSnapshotFailedError` if it fails to capture, or `SandboxSnapshotWaitTimeoutError`
   * after `timeoutMs`.
   */
  async waitUntilAvailable(
    input: SandboxSnapshotGetInput,
    options: SandboxWaitOptions = {},
  ): Promise<SandboxSnapshot> {
    return pollUntil((signal) => this.get(input, signal), availableSnapshot, {
      timeoutMs: options.timeoutMs ?? DEFAULT_SNAPSHOT_WAIT_TIMEOUT_MS,
      intervalMs: options.intervalMs ?? DEFAULT_WAIT_INTERVAL_MS,
      signal: options.signal,
      timeoutError: (last) =>
        new SandboxSnapshotWaitTimeoutError(
          `Timed out waiting for snapshot ${input.snapshotId} to be available`,
          input.snapshotId,
          options.timeoutMs ?? DEFAULT_SNAPSHOT_WAIT_TIMEOUT_MS,
          last?.status,
        ),
    });
  }

  async list({
    sandboxGroupId,
    status,
    cursor,
    limit,
    ownerId,
  }: SandboxSnapshotListInput): Promise<SandboxSnapshotWithCursor[]> {
    const owner = resolveOwnerId(ownerId, this.defaultOwnerId);
    return unwrap(
      await this.apiClient.GET("/sandbox-groups/{sandboxGroupId}/snapshots", {
        params: {
          path: { sandboxGroupId },
          query: { ownerId: owner, status, cursor, limit },
        },
      }),
      inWorkspace("Failed to list snapshots", owner),
    );
  }

  async delete({ sandboxGroupId, snapshotId, ownerId }: SandboxSnapshotDeleteInput): Promise<void> {
    const { error, response } = await this.apiClient.DELETE(
      "/sandbox-groups/{sandboxGroupId}/snapshots/{snapshotId}",
      {
        params: {
          path: { sandboxGroupId, snapshotId },
          ...optionalOwnerIdQuery(ownerId, this.defaultOwnerId),
        },
      },
    );
    if (error !== undefined || !response.ok) {
      throw getSnapshotApiError(error, response, "Failed to delete snapshot");
    }
  }
}

export class SandboxBuildsClient {
  constructor(private readonly apiClient: Client<paths>) {}

  /**
   * Returns once the build has started; poll `get()` for `succeeded` or `failed`. A name and
   * digest the group already has, or is building, returns that build instead of starting another.
   */
  async create({
    sandboxGroupId,
    name,
    sourceImage,
    registryCredential,
  }: SandboxBuildCreateInput): Promise<SandboxBuild> {
    const body: components["schemas"]["sandboxBuildPOST"] = {
      name,
      sourceImage,
      ...(registryCredential ? { registryCredential } : {}),
    };
    return unwrap(
      await this.apiClient.POST("/sandbox-groups/{sandboxGroupId}/builds", {
        params: { path: { sandboxGroupId } },
        body,
      }),
      "Failed to create build",
    );
  }

  async get({ sandboxGroupId, buildId }: SandboxBuildGetInput): Promise<SandboxBuild> {
    return unwrap(
      await this.apiClient.GET("/sandbox-groups/{sandboxGroupId}/builds/{buildId}", {
        params: { path: { sandboxGroupId, buildId } },
      }),
      "Failed to get build",
    );
  }
}

export class SandboxesClient {
  public readonly snapshots: SandboxSnapshotsClient;
  public readonly builds: SandboxBuildsClient;
  private readonly defaultOwnerId?: string;
  private readonly defaultRegion?: string;

  constructor(
    private readonly apiClient: Client<paths>,
    defaultOwnerId?: string,
    defaultRegion?: string,
  ) {
    this.defaultOwnerId = defaultOwnerId;
    this.defaultRegion = defaultRegion;
    this.snapshots = new SandboxSnapshotsClient(apiClient, defaultOwnerId);
    this.builds = new SandboxBuildsClient(apiClient);
  }

  private resolveOwnerId(ownerId?: `tea-${string}`): `tea-${string}` {
    return resolveOwnerId(ownerId, this.defaultOwnerId);
  }

  /**
   * Waits until the sandbox is `running`, so it can run commands. Throws
   * `SandboxNotRunningError` if it ends or is suspended first, or `SandboxWaitTimeoutError`
   * after `timeoutMs`. Neither error terminates the sandbox.
   */
  async waitUntilRunning(
    sandboxId: string,
    options: SandboxWaitOptions & { ownerId?: `tea-${string}` } = {},
  ): Promise<Sandbox> {
    return pollUntil((signal) => this.get(sandboxId, options.ownerId, signal), runningSandbox, {
      timeoutMs: options.timeoutMs ?? DEFAULT_SANDBOX_WAIT_TIMEOUT_MS,
      intervalMs: options.intervalMs ?? DEFAULT_WAIT_INTERVAL_MS,
      signal: options.signal,
      timeoutError: (last) =>
        new SandboxWaitTimeoutError(
          `Timed out waiting for sandbox ${sandboxId} to be running`,
          sandboxId,
          options.timeoutMs ?? DEFAULT_SANDBOX_WAIT_TIMEOUT_MS,
          last?.status,
        ),
    });
  }

  async get(sandboxId: string, ownerId?: `tea-${string}`, signal?: AbortSignal) {
    return unwrap(
      await this.apiClient.GET("/sandboxes/{sandboxId}", {
        params: {
          path: { sandboxId },
          query: { ownerId: this.resolveOwnerId(ownerId) },
        },
        ...(signal ? { signal } : {}),
      }),
      "Failed to get sandbox",
    );
  }

  async create(input: SandboxCreateInput = {}): Promise<Sandbox> {
    const wait = resolveCreateWait(input.wait, DEFAULT_SANDBOX_WAIT_TIMEOUT_MS);
    const region = input.region ?? this.defaultRegion;
    const ownerId = this.resolveOwnerId(input.ownerId);
    const body = {
      ownerId,
      ...(input.plan ? { plan: input.plan } : {}),
      ...(input.timeoutSeconds === undefined ? {} : { timeoutSeconds: input.timeoutSeconds }),
      ...(input.idleTimeoutSeconds === undefined
        ? {}
        : { idleTimeoutSeconds: input.idleTimeoutSeconds }),
      ...(region ? { region } : {}),
      ...(input.networkPolicy ? { networkPolicy: input.networkPolicy } : {}),
      ...(input.env ? { env: input.env } : {}),
      ...(input.snapshotId ? { snapshotId: input.snapshotId } : {}),
      ...(input.snapshotName === undefined ? {} : { snapshotName: input.snapshotName }),
      ...(input.buildId === undefined ? {} : { buildId: input.buildId }),
      ...(input.buildName === undefined ? {} : { buildName: input.buildName }),
    } as components["schemas"]["sandboxPOST"];
    const sandbox = unwrap(
      await this.apiClient.POST("/sandboxes", { body }),
      inWorkspace("Failed to create sandbox", ownerId),
    );
    if (!wait) {
      return sandbox;
    }
    // The sandbox exists from here on, so every failure must give the caller its ID.
    try {
      return (
        runningSandbox(sandbox) ?? (await this.waitUntilRunning(sandbox.id, { ...wait, ownerId }))
      );
    } catch (err) {
      const reason = err instanceof Error ? err.message : String(err);
      throw new SandboxCreateWaitError(
        `Created sandbox ${sandbox.id}, but it is not running: ${reason}`,
        sandbox.id,
        err,
      );
    }
  }

  async list({
    ownerId,
    cursor,
    limit,
    status,
  }: {
    ownerId?: `tea-${string}`;
    cursor?: string;
    limit?: number;
    status?: components["schemas"]["sandboxStatus"][];
  } = {}) {
    const owner = this.resolveOwnerId(ownerId);
    return unwrap(
      await this.apiClient.GET("/sandboxes", {
        params: {
          query: {
            ownerId: owner,
            cursor,
            limit,
            status,
          },
        },
      }),
      inWorkspace("Failed to list sandboxes", owner),
    );
  }

  async listGroups({ ownerId }: SandboxGroupListInput = {}): Promise<SandboxGroupWithCursor[]> {
    const owner = this.resolveOwnerId(ownerId);
    return unwrap(
      await this.apiClient.GET("/sandbox-groups", {
        params: {
          query: {
            ownerId: owner,
          },
        },
      }),
      inWorkspace("Failed to list sandbox groups", owner),
    );
  }

  async terminate(sandboxId: string, ownerId?: `tea-${string}`): Promise<void> {
    const { error, response } = await this.apiClient.POST("/sandboxes/{sandboxId}/terminate", {
      params: {
        path: { sandboxId },
        query: { ownerId: this.resolveOwnerId(ownerId) },
      },
    });
    if (error !== undefined || !response.ok) {
      throw getTypedApiError(error, response, "Failed to terminate sandbox");
    }
  }

  async upload(
    sandboxId: string,
    path: string,
    data: SandboxUploadData,
    ownerId?: `tea-${string}`,
    options: SandboxUploadOptions = {},
  ): Promise<void> {
    if (options.signal?.aborted) {
      throw new AbortError();
    }

    const tokenResponse = await this.getFileConnectToken(sandboxId, path, "upload", ownerId);
    let response: Response;
    try {
      response = await fetch(tokenResponse.uri, {
        method: tokenResponse.method,
        headers: {
          Authorization: `Bearer ${tokenResponse.token}`,
          "Content-Type": options.contentType ?? "application/octet-stream",
          "User-Agent": getUserAgent(),
        },
        body: data as Buffer | Uint8Array | string,
        duplex: "half",
        signal: options.signal,
      });
      if (!response.ok) {
        throw await getResponseError(response, "Failed to upload sandbox file");
      }
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        throw new AbortError();
      }
      throw err;
    }
  }

  async download(
    sandboxId: string,
    path: string,
    ownerId?: `tea-${string}`,
    signal?: AbortSignal,
  ): Promise<SandboxDownload> {
    if (signal?.aborted) {
      throw new AbortError();
    }

    const tokenResponse = await this.getFileConnectToken(sandboxId, path, "download", ownerId);
    try {
      const response = await fetch(tokenResponse.uri, {
        method: tokenResponse.method,
        headers: {
          Authorization: `Bearer ${tokenResponse.token}`,
          "User-Agent": getUserAgent(),
        },
        signal,
      });

      if (!response.ok) {
        throw await getResponseError(response, "Failed to download sandbox file");
      }

      const data = Buffer.from(await response.arrayBuffer());
      return {
        data,
        size: data.byteLength,
        contentType: response.headers.get("Content-Type") ?? undefined,
      };
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        throw new AbortError();
      }
      throw err;
    }
  }

  private async getRunConnectToken(
    sandboxId: string,
    operation: SandboxConnectOperation,
    ownerId?: `tea-${string}`,
    command?: string,
  ): Promise<components["schemas"]["sandboxConnectResponse"]> {
    const context = "Failed to get connect token";
    try {
      return unwrap(
        await this.apiClient.POST(`/sandboxes/{sandboxId}/runs/{operation}/token`, {
          params: {
            path: {
              sandboxId,
              operation,
            },
            query: {
              ownerId: this.resolveOwnerId(ownerId),
            },
          },
          ...(command ? { body: { command } } : {}),
        }),
        context,
      );
    } catch (err) {
      throw await this.explainEndedSandbox(err, sandboxId, ownerId, context);
    }
  }

  private async getFileConnectToken(
    sandboxId: string,
    path: string,
    operation: SandboxFileOperation,
    ownerId?: `tea-${string}`,
  ): Promise<components["schemas"]["sandboxConnectResponse"]> {
    const context = "Failed to get file connect token";
    try {
      return unwrap(
        await this.apiClient.POST("/sandboxes/{sandboxId}/files/{operation}/token", {
          params: {
            path: { sandboxId, operation },
            query: {
              ownerId: this.resolveOwnerId(ownerId),
              path: cleanSandboxPath(path),
            },
          },
        }),
        context,
      );
    } catch (err) {
      throw await this.explainEndedSandbox(err, sandboxId, ownerId, context);
    }
  }

  /**
   * The connect token endpoint returns a bare 404 both for a sandbox that isn't ready yet and
   * for one that has ended. Only the first is worth retrying, so look up the sandbox and name
   * the second.
   */
  private async explainEndedSandbox(
    err: unknown,
    sandboxId: string,
    ownerId: `tea-${string}` | undefined,
    context: string,
  ): Promise<unknown> {
    if (!(err instanceof ClientError) || err.statusCode !== 404) {
      return err;
    }
    let sandbox: Sandbox;
    try {
      sandbox = await this.get(sandboxId, ownerId);
    } catch {
      return err;
    }
    if (sandbox.status !== "terminated" && sandbox.status !== "errored") {
      return err;
    }
    const ended = sandbox.status === "terminated" ? "was terminated" : "errored";
    const at = sandbox.terminatedAt ? ` at ${sandbox.terminatedAt}` : "";
    return new SandboxEndedError(
      `${context}: sandbox ${sandboxId} ${ended}${at}`,
      err.statusCode,
      sandbox.status,
      err.response,
      err.code,
    );
  }

  async exec(
    sandboxId: string,
    command: string,
    ownerId?: `tea-${string}`,
    signal?: AbortSignal,
  ): Promise<AsyncGenerator<SandboxExecEvent>> {
    if (signal?.aborted) {
      throw new AbortError();
    }

    const tokenResponse = await this.getRunConnectToken(sandboxId, "stream", ownerId, command);

    let response: Response;
    try {
      response = await fetch(tokenResponse.uri, {
        method: tokenResponse.method,
        headers: this.getStreamHeaders(tokenResponse.token),
        body: JSON.stringify({ command }),
        signal,
      });
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        throw new AbortError();
      }
      throw err;
    }

    if (!response.ok) {
      throw await getResponseError(response, "Failed to execute sandbox command");
    }
    if (!response.body) {
      throw new RenderError("Sandbox exec stream response did not include a response body.");
    }

    return this.iterExecEvents(response.body);
  }

  private async *iterExecEvents(
    body: ReadableStream<Uint8Array>,
  ): AsyncGenerator<SandboxExecEvent> {
    try {
      let sawTerminalEvent = false;
      for await (const event of parseSseStream(body)) {
        switch (event.event) {
          case "output": {
            const output = parseEventData<SandboxExecOutputEvent>(event);
            yield { type: "output", ...output };
            break;
          }
          case "exit": {
            const exit = parseEventData<SandboxExecExitEvent>(event);
            sawTerminalEvent = true;
            yield { type: "exit", ...exit };
            return;
          }
          case "error": {
            const streamError = parseEventData<SandboxExecErrorEvent>(event);
            sawTerminalEvent = true;
            throw new SandboxExecStreamError(streamError.status, streamError.message);
          }
          default:
            throw new RenderError(`Unknown sandbox exec stream event "${event.event}".`);
        }
      }
      if (!sawTerminalEvent) {
        throw new RenderError("Sandbox exec stream ended without a terminal event.");
      }
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        throw new AbortError();
      }
      throw err;
    }
  }

  private getStreamHeaders(connectToken: string): Record<string, string> {
    return {
      Accept: "text/event-stream",
      "Content-Type": "application/json",
      "User-Agent": getUserAgent(),
      Authorization: `Bearer ${connectToken}`,
    };
  }
}

type SseEvent = {
  event: string;
  data: string;
};

async function* parseSseStream(stream: ReadableStream<Uint8Array>): AsyncGenerator<SseEvent> {
  const reader = stream.getReader();
  try {
    const decoder = new TextDecoder();
    let buffer = "";
    let event = "";
    let data = "";

    const processLine = (line: string): SseEvent | null => {
      if (line === "") {
        if (!event && !data) {
          return null;
        }
        const complete = { event, data };
        event = "";
        data = "";
        return complete;
      }
      if (line.startsWith("event:")) {
        event = line.slice("event:".length).trim();
        return null;
      }
      if (line.startsWith("data:")) {
        if (data) {
          data += "\n";
        }
        data += line.slice("data:".length).replace(LEADING_SPACE, "");
      }
      return null;
    };

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      let newlineIndex = buffer.indexOf("\n");
      while (newlineIndex !== -1) {
        const line = buffer.slice(0, newlineIndex).replace(TRAILING_CARRIAGE_RETURN, "");
        buffer = buffer.slice(newlineIndex + 1);
        const complete = processLine(line);
        if (complete) {
          yield complete;
        }
        newlineIndex = buffer.indexOf("\n");
      }
    }

    buffer += decoder.decode();
    if (buffer) {
      const trailing = processLine(buffer.replace(TRAILING_CARRIAGE_RETURN, ""));
      if (trailing) {
        yield trailing;
      }
    }
    const complete = processLine("");
    if (complete) {
      yield complete;
    }
  } finally {
    await reader.cancel().catch(() => {});
    reader.releaseLock();
  }
}

function parseEventData<T>(event: SseEvent): T {
  try {
    return JSON.parse(event.data) as T;
  } catch (err) {
    const reason = err instanceof Error ? err.message : String(err);
    throw new RenderError(`Failed to parse sandbox exec "${event.event}" event data: ${reason}`);
  }
}

async function getResponseError(response: Response, context: string): Promise<Error> {
  const text = await response.text();
  return getApiError(text || response.statusText, response, context);
}

function unwrap<T>(
  { data, error, response }: { data?: T; error?: unknown; response: Response },
  context: string,
  toError: (error: unknown, response: Response, context: string) => Error = getTypedApiError,
): T {
  if (error !== undefined || !response.ok || data === undefined) {
    throw toError(error, response, context);
  }
  return data;
}

function getTypedApiError(error: unknown, response: Response, context: string): Error {
  const body = error as { message?: unknown; code?: unknown } | null | undefined;
  const message =
    typeof body?.message === "string"
      ? body.message
      : error
        ? JSON.stringify(error)
        : response.statusText;
  const code = typeof body?.code === "string" ? body.code : undefined;
  return getApiError(message, response, context, code);
}

function getSnapshotApiError(error: unknown, response: Response, context: string): Error {
  const apiError = getTypedApiError(error, response, context);
  if (apiError instanceof ClientError && apiError.statusCode === 404) {
    return new SandboxSnapshotNotFoundError(
      apiError.message,
      apiError.statusCode,
      apiError.response,
      apiError.code,
    );
  }
  return apiError;
}
