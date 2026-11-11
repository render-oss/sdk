import { stat } from "node:fs/promises";
import { posix } from "node:path";
import type { Readable } from "node:stream";
import type { Client } from "openapi-fetch";

import {
  AbortError,
  ClientError,
  RenderError,
  SandboxCreateWaitError,
  SandboxCredentialNotFoundError,
  SandboxEndedError,
  SandboxImageFailedError,
  SandboxImageWaitTimeoutError,
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
import {
  downloadLimit,
  putFile,
  readLimitedBody,
  saveLimitedBody,
  toDownloadOptions,
} from "./files.js";
import type { SandboxPlan } from "./types.js";

export type { SandboxPlan } from "./types.js";

const DEFAULT_DOWNLOAD_MAX_BYTES = 256 * 1024 * 1024;
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

export type SandboxDownloadOptions = {
  /**
   * The largest download to hold in memory, in bytes. Defaults to 256 MiB. A larger download
   * throws `SandboxDownloadTooLargeError`.
   */
  maxSizeBytes?: number;
  signal?: AbortSignal;
};

export type SandboxCopyToOptions = {
  localPath: string;
  remotePath: string;
  ownerId?: `tea-${string}`;
  signal?: AbortSignal;
};

export type SandboxCopyFromOptions = {
  remotePath: string;
  localPath: string;
  ownerId?: `tea-${string}`;
  /**
   * The largest file to copy, in bytes. No limit by default. A larger download throws
   * `SandboxDownloadTooLargeError`.
   */
  maxSizeBytes?: number;
  signal?: AbortSignal;
};

export type SandboxDownload = {
  /** Backed by an `ArrayBuffer`, so it passes to Web and Bun APIs that take `Uint8Array<ArrayBuffer>`. */
  data: ReturnType<typeof Buffer.from>;
  size: number;
  contentType?: string;
};

export type SandboxCopyFromResult = {
  localPath: string;
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
      image?: never;
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
      image?: never;
      buildId?: never;
      buildName?: never;
    }
  | {
      snapshotId?: never;
      snapshotName?: never;
      /**
       * Start from an image imported with `images.import()` instead of the base image. An image ID
       * (`sbb-` and 20 characters, like `sbb-cph1rs3idesc73a2b2mg`) pins that version; any other
       * value is a name and uses the newest `succeeded` version with that name in the sandbox
       * group.
       */
      image?: string;
      buildId?: never;
      buildName?: never;
    }
  | {
      snapshotId?: never;
      snapshotName?: never;
      image?: never;
      /** @deprecated Use `image` with the image ID. */
      buildId?: string;
      buildName?: never;
    }
  | {
      snapshotId?: never;
      snapshotName?: never;
      image?: never;
      buildId?: never;
      /** @deprecated Use `image` with the image name. */
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
  /** Omit to use the workspace's default group. */
  sandboxGroupId?: string;
  /**
   * A label for the sandbox, like `my-agent`. Names aren't unique, so use the sandbox ID to
   * address it. At most 64 characters, and it can't start with `sbx-`.
   */
  name?: string;
  ownerId?: `tea-${string}`;
  plan?: SandboxPlan | (string & {});
  /** Maximum sandbox lifetime in seconds. 0 disables the lifetime limit. The API defaults to 86400 (24 hours). */
  timeoutSeconds?: number;
  /**
   * Seconds of inactivity before the sandbox is suspended. Use 0 to disable automatic idle
   * suspension; positive values must be at least 300. The API defaults to 900.
   */
  idleTimeoutSeconds?: number;
  /** @deprecated The API uses the sandbox group's region. */
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

/** A sandbox image as returned by the API. */
export type SandboxImage = components["schemas"]["sandboxBuild"];

/** `pending` or `running` until the import finishes, then `succeeded` or `failed`. */
export type SandboxImageStatus = components["schemas"]["sandboxBuildStatus"];

/** The OCI image an import converts, as the registry resolved it. */
export type SandboxImageSource = SandboxImage["source"];

/** Pulls `source` from a private registry. Used for that import only and never stored. */
export type SandboxRegistryCredentials = NonNullable<
  components["schemas"]["sandboxBuildPOST"]["registryCredential"]
>;

/** Options for importing an OCI image so sandboxes can start from it. */
export type SandboxImageImportInput = {
  sandboxGroupId: string;
  /**
   * Names the image. Every version of an image shares it, and `create({ image: name })` starts
   * from the newest one that succeeded. 1 to 255 characters.
   */
  name: string;
  /** The image to import, by tag or digest, like `ghcr.io/acme/agent-runtime:v1`. Must be linux/amd64. */
  source: string;
  registryCredentials?: SandboxRegistryCredentials;
};

/** Options for retrieving an image. */
export type SandboxImageGetInput = {
  sandboxGroupId: string;
  imageId: string;
};

/** Options for listing the images in a sandbox group, newest first. */
export type SandboxImageListInput = {
  sandboxGroupId: string;
  /** Return only versions of the image with this name. */
  name?: string;
  status?: SandboxImageStatus[];
  cursor?: string;
  /** 1 to 100. */
  limit?: number;
};

/** An image in a list, with the cursor to pass to `list()` for the page after it. */
export type SandboxImageWithCursor = { image: SandboxImage; cursor: string };

/** @deprecated Use `SandboxImage`. */
export type SandboxBuild = SandboxImage;

/** @deprecated Use `SandboxImageStatus`. */
export type SandboxBuildStatus = SandboxImageStatus;

/** @deprecated Use `SandboxImageSource`. */
export type SandboxBuildSource = SandboxImageSource;

/** @deprecated Use `SandboxRegistryCredentials`. */
export type SandboxRegistryCredential = SandboxRegistryCredentials;

/** @deprecated Use `SandboxImageImportInput` with `images.import()`. */
export type SandboxBuildCreateInput = {
  sandboxGroupId: string;
  name: string;
  sourceImage: string;
  registryCredential?: SandboxRegistryCredentials;
};

/** @deprecated Use `SandboxImageGetInput` with `images.get()`. */
export type SandboxBuildGetInput = {
  sandboxGroupId: string;
  buildId: string;
};

/**
 * A credential that Render adds to matching requests from a sandbox group's sandboxes, so code in
 * the sandbox never sees the secret. The API never returns the secret value.
 */
export type SandboxCredential = components["schemas"]["sandboxCredential"];

/**
 * How a credential is added to a matching request. `name` is the header, cookie or query
 * parameter to set; every `type` but `basic` requires it, and `basic` rejects it. `template` wraps
 * the secret, like `Bearer ${SECRET}`; omit it to send the secret as is. `basic` expects the
 * secret, after the template, in `username:password` form.
 */
export type SandboxCredentialInjection = components["schemas"]["sandboxCredentialInjection"];

/**
 * One saved configuration of a credential. Two versions in the same sandbox group with the same
 * `fingerprint` have the same routing, injection and secret value.
 */
export type SandboxCredentialVersion = components["schemas"]["sandboxCredentialVersion"];

/** Options for creating a credential. */
export type SandboxCredentialCreateInput = {
  sandboxGroupId: string;
  /** A URL-safe name, case sensitive and unique within the group. */
  credentialId: string;
  /** The exact public hostname the credential applies to, like `api.openai.com`. */
  domain: string;
  /** The secret, at most 5 KiB. */
  value: string;
  injection: SandboxCredentialInjection;
  /** Narrows the methods that match, like `["POST"]`. Omit to match any. */
  methods?: string[];
  /**
   * Narrows the paths that match, like `["/v1/**"]`. `*` matches one path segment and `**` one or
   * more. Omit to match any.
   */
  paths?: string[];
  /** Defaults to `true`. */
  enabled?: boolean;
};

/** Options for retrieving a credential or listing its versions. */
export type SandboxCredentialGetInput = {
  sandboxGroupId: string;
  credentialId: string;
};

/** Options for listing the credentials in a sandbox group. */
export type SandboxCredentialListInput = {
  sandboxGroupId: string;
};

/**
 * Options for changing a credential. Fields left out keep their current value. An empty
 * `methods` or `paths` array clears that filter, so the credential matches any method or path.
 */
export type SandboxCredentialUpdateInput = {
  sandboxGroupId: string;
  credentialId: string;
  /** Needs an admin. */
  domain?: string;
  /** Needs an admin. Always creates a new version, even when the value is unchanged. */
  value?: string;
  injection?: SandboxCredentialInjection;
  methods?: string[];
  paths?: string[];
  enabled?: boolean;
};

/** Options for deleting a credential. Deleting a credential that does not exist succeeds. */
export type SandboxCredentialDeleteInput = {
  sandboxGroupId: string;
  credentialId: string;
};

/** Options for making an earlier version of a credential current again. */
export type SandboxCredentialRestoreInput = {
  sandboxGroupId: string;
  credentialId: string;
  versionId: number;
};

/** A sandbox group as returned by the API. */
export type SandboxGroup = components["schemas"]["sandboxGroup"];

/** A sandbox group paired with its pagination cursor. */
export type SandboxGroupWithCursor = components["schemas"]["sandboxGroupWithCursor"];

/** Options for listing sandbox groups. */
export type SandboxGroupListInput = {
  cursor?: string;
  limit?: number;
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
/** Matches the CLI's `sandbox-groups images import --wait`. */
const DEFAULT_IMAGE_WAIT_TIMEOUT_MS = 10 * 60_000;

/** The format of an image ID; `create({ image })` treats anything else as a name. */
const IMAGE_ID_PATTERN = /^sbb-[0-9a-v]{20}$/;

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
 * Returns the image if it has `succeeded`, or `undefined` if its import is still `pending` or
 * `running`.
 * Throws `SandboxImageFailedError` if the import failed.
 */
function readyImage(image: SandboxImage): SandboxImage | undefined {
  if (image.status === "succeeded") return image;
  if (image.status === "failed") {
    throw new SandboxImageFailedError(
      `Image ${image.id} failed to import${image.failureReason ? `: ${image.failureReason}` : ""}`,
      image.id,
      image.failureReason ?? undefined,
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

export class SandboxImagesClient {
  constructor(private readonly apiClient: Client<paths>) {}

  /**
   * Starts importing an OCI image so sandboxes can start from it. Returns once the import has
   * started; call `waitUntilReady()` to wait for it to succeed. A name and digest the group
   * already has, or is importing, returns that image instead of starting another.
   */
  async import({
    sandboxGroupId,
    name,
    source,
    registryCredentials,
  }: SandboxImageImportInput): Promise<SandboxImage> {
    const body: components["schemas"]["sandboxBuildPOST"] = {
      name,
      sourceImage: source,
      ...(registryCredentials ? { registryCredential: registryCredentials } : {}),
    };
    return unwrap(
      await this.apiClient.POST("/sandbox-groups/{sandboxGroupId}/builds", {
        params: { path: { sandboxGroupId } },
        body,
      }),
      "Failed to import image",
    );
  }

  async get(
    { sandboxGroupId, imageId }: SandboxImageGetInput,
    signal?: AbortSignal,
  ): Promise<SandboxImage> {
    return unwrap(
      await this.apiClient.GET("/sandbox-groups/{sandboxGroupId}/builds/{buildId}", {
        params: { path: { sandboxGroupId, buildId: imageId } },
        ...(signal ? { signal } : {}),
      }),
      "Failed to get image",
    );
  }

  /** Lists the images in a sandbox group, newest first. Each version of a name is its own image. */
  async list({
    sandboxGroupId,
    name,
    status,
    cursor,
    limit,
  }: SandboxImageListInput): Promise<SandboxImageWithCursor[]> {
    const page = unwrap(
      await this.apiClient.GET("/sandbox-groups/{sandboxGroupId}/builds", {
        params: {
          path: { sandboxGroupId },
          query: { name, status, cursor, limit },
        },
      }),
      "Failed to list images",
    );
    return page.map(({ build, cursor }) => ({ image: build, cursor }));
  }

  /**
   * Waits until the image has `succeeded`, so sandboxes can start from it. Throws
   * `SandboxImageFailedError` if the import fails, or `SandboxImageWaitTimeoutError` after
   * `timeoutMs` (10 minutes by default).
   */
  async waitUntilReady(
    input: SandboxImageGetInput,
    options: SandboxWaitOptions = {},
  ): Promise<SandboxImage> {
    return pollUntil((signal) => this.get(input, signal), readyImage, {
      timeoutMs: options.timeoutMs ?? DEFAULT_IMAGE_WAIT_TIMEOUT_MS,
      intervalMs: options.intervalMs ?? DEFAULT_WAIT_INTERVAL_MS,
      signal: options.signal,
      timeoutError: (last) =>
        new SandboxImageWaitTimeoutError(
          `Timed out waiting for image ${input.imageId} to be ready`,
          input.imageId,
          options.timeoutMs ?? DEFAULT_IMAGE_WAIT_TIMEOUT_MS,
          last?.status,
        ),
    });
  }
}

/** @deprecated Use `SandboxImagesClient`, via `sandboxes.images`. */
export class SandboxBuildsClient {
  private readonly images: SandboxImagesClient;

  constructor(apiClient: Client<paths>) {
    this.images = new SandboxImagesClient(apiClient);
  }

  /** @deprecated Use `images.import()`. */
  async create({
    sandboxGroupId,
    name,
    sourceImage,
    registryCredential,
  }: SandboxBuildCreateInput): Promise<SandboxImage> {
    return this.images.import({
      sandboxGroupId,
      name,
      source: sourceImage,
      ...(registryCredential ? { registryCredentials: registryCredential } : {}),
    });
  }

  /** @deprecated Use `images.get()`. */
  async get({ sandboxGroupId, buildId }: SandboxBuildGetInput): Promise<SandboxImage> {
    return this.images.get({ sandboxGroupId, imageId: buildId });
  }
}

/**
 * Credentials that Render adds to requests from a sandbox group's sandboxes, via
 * `sandboxes.credentials`. Creating, deleting and restoring a credential, and changing its domain
 * or value, need an admin of the workspace.
 */
export class SandboxCredentialsClient {
  constructor(private readonly apiClient: Client<paths>) {}

  /**
   * Creates a credential in a sandbox group. A group holds at most 25 credentials. Throws a
   * `ClientError` with status 409 if the group already has `credentialId`.
   */
  async create({
    sandboxGroupId,
    credentialId,
    domain,
    value,
    injection,
    methods,
    paths,
    enabled,
  }: SandboxCredentialCreateInput): Promise<SandboxCredential> {
    const body: components["schemas"]["sandboxCredentialCreate"] = {
      id: credentialId,
      domain,
      value,
      injection,
      enabled: enabled ?? true,
      ...(methods ? { methods } : {}),
      ...(paths ? { paths } : {}),
    };
    return unwrap(
      await this.apiClient.POST("/sandbox-groups/{sandboxGroupId}/credentials", {
        params: { path: { sandboxGroupId } },
        body,
      }),
      `Failed to create credential ${credentialId}`,
    );
  }

  /** Retrieves a credential. Throws `SandboxCredentialNotFoundError` if it does not exist. */
  async get({
    sandboxGroupId,
    credentialId,
  }: SandboxCredentialGetInput): Promise<SandboxCredential> {
    return unwrap(
      await this.apiClient.GET("/sandbox-groups/{sandboxGroupId}/credentials/{credentialId}", {
        params: { path: { sandboxGroupId, credentialId } },
      }),
      `Failed to get credential ${credentialId}`,
      getCredentialApiError,
    );
  }

  /** Lists every credential in a sandbox group, sorted by ID. */
  async list({ sandboxGroupId }: SandboxCredentialListInput): Promise<SandboxCredential[]> {
    return unwrap(
      await this.apiClient.GET("/sandbox-groups/{sandboxGroupId}/credentials", {
        params: { path: { sandboxGroupId } },
      }),
      "Failed to list credentials",
    );
  }

  /** Changes a credential. Throws `SandboxCredentialNotFoundError` if it does not exist. */
  async update({
    sandboxGroupId,
    credentialId,
    domain,
    value,
    injection,
    methods,
    paths,
    enabled,
  }: SandboxCredentialUpdateInput): Promise<SandboxCredential> {
    const body: components["schemas"]["sandboxCredentialUpdate"] = {
      ...(domain === undefined ? {} : { domain }),
      ...(value === undefined ? {} : { value }),
      ...(injection === undefined ? {} : { injection }),
      ...(methods === undefined ? {} : { methods }),
      ...(paths === undefined ? {} : { paths }),
      ...(enabled === undefined ? {} : { enabled }),
    };
    return unwrap(
      await this.apiClient.PATCH("/sandbox-groups/{sandboxGroupId}/credentials/{credentialId}", {
        params: { path: { sandboxGroupId, credentialId } },
        body,
      }),
      `Failed to update credential ${credentialId}`,
      getCredentialApiError,
    );
  }

  /** Deletes a credential and its versions. Deleting a credential that does not exist succeeds. */
  async delete({ sandboxGroupId, credentialId }: SandboxCredentialDeleteInput): Promise<void> {
    const { error, response } = await this.apiClient.DELETE(
      "/sandbox-groups/{sandboxGroupId}/credentials/{credentialId}",
      { params: { path: { sandboxGroupId, credentialId } } },
    );
    if (error !== undefined || !response.ok) {
      // A missing credential is not an error here, so a 404 is about the group.
      throw getTypedApiError(error, response, `Failed to delete credential ${credentialId}`);
    }
  }

  /**
   * Lists the versions of a credential, newest first. The API keeps the current configuration and
   * the three most recently active earlier ones. Throws `SandboxCredentialNotFoundError` if the
   * credential does not exist.
   */
  async listVersions({
    sandboxGroupId,
    credentialId,
  }: SandboxCredentialGetInput): Promise<SandboxCredentialVersion[]> {
    return unwrap(
      await this.apiClient.GET(
        "/sandbox-groups/{sandboxGroupId}/credentials/{credentialId}/versions",
        { params: { path: { sandboxGroupId, credentialId } } },
      ),
      `Failed to list versions of credential ${credentialId}`,
      getCredentialApiError,
    );
  }

  /**
   * Makes an earlier version's configuration and value current again, as a new version whose
   * `restoredFromVersionId` is `versionId`. Throws `SandboxCredentialNotFoundError` if the
   * credential or the version does not exist.
   */
  async restore({
    sandboxGroupId,
    credentialId,
    versionId,
  }: SandboxCredentialRestoreInput): Promise<SandboxCredential> {
    return unwrap(
      await this.apiClient.POST(
        "/sandbox-groups/{sandboxGroupId}/credentials/{credentialId}/restore",
        { params: { path: { sandboxGroupId, credentialId } }, body: { versionId } },
      ),
      `Failed to restore credential ${credentialId} to version ${versionId}`,
      getCredentialApiError,
    );
  }
}

export class SandboxesClient {
  public readonly snapshots: SandboxSnapshotsClient;
  public readonly images: SandboxImagesClient;
  public readonly credentials: SandboxCredentialsClient;
  /** @deprecated Use `images`. */
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
    this.images = new SandboxImagesClient(apiClient);
    this.credentials = new SandboxCredentialsClient(apiClient);
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
    const ownerId = this.resolveOwnerId(input.ownerId);
    const body = {
      ownerId,
      ...(input.plan ? { plan: input.plan } : {}),
      ...(input.sandboxGroupId === undefined ? {} : { sandboxGroupId: input.sandboxGroupId }),
      ...(input.name === undefined ? {} : { name: input.name }),
      ...(input.timeoutSeconds === undefined ? {} : { timeoutSeconds: input.timeoutSeconds }),
      ...(input.idleTimeoutSeconds === undefined
        ? {}
        : { idleTimeoutSeconds: input.idleTimeoutSeconds }),
      ...(input.networkPolicy ? { networkPolicy: input.networkPolicy } : {}),
      ...(input.env ? { env: input.env } : {}),
      ...(input.snapshotId ? { snapshotId: input.snapshotId } : {}),
      ...(input.snapshotName === undefined ? {} : { snapshotName: input.snapshotName }),
      ...(input.image === undefined
        ? {}
        : IMAGE_ID_PATTERN.test(input.image)
          ? { buildId: input.image }
          : { buildName: input.image }),
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
    sandboxGroupId,
    name,
  }: {
    ownerId?: `tea-${string}`;
    cursor?: string;
    limit?: number;
    sandboxGroupId?: string;
    status?: components["schemas"]["sandboxStatus"][];
    /** Return only sandboxes with exactly this name. Names aren't unique, so this can match several. */
    name?: string;
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
            sandboxGroupId,
            name,
          },
        },
      }),
      inWorkspace("Failed to list sandboxes", owner),
    );
  }

  async listGroups({
    ownerId,
    cursor,
    limit,
  }: SandboxGroupListInput = {}): Promise<SandboxGroupWithCursor[]> {
    const owner = this.resolveOwnerId(ownerId);
    return unwrap(
      await this.apiClient.GET("/sandbox-groups", {
        params: {
          query: {
            ownerId: owner,
            cursor,
            limit,
          },
        },
      }),
      inWorkspace("Failed to list sandbox groups", owner),
    );
  }

  async createGroup(input: {
    name: string;
    region?: string;
    ownerId?: `tea-${string}`;
  }): Promise<SandboxGroup> {
    const ownerId = this.resolveOwnerId(input.ownerId);
    return unwrap(
      await this.apiClient.POST("/sandbox-groups", {
        body: { ...input, ownerId, region: input.region ?? this.defaultRegion ?? "oregon" },
      }),
      inWorkspace("Failed to create sandbox group", ownerId),
    );
  }

  async getGroup(sandboxGroupId: string): Promise<SandboxGroup> {
    return unwrap(
      await this.apiClient.GET("/sandbox-groups/{sandboxGroupId}", {
        params: { path: { sandboxGroupId } },
      }),
      "Failed to get sandbox group",
    );
  }

  /** Returns the effective limit after applying Render's cap. */
  async updateGroup(sandboxGroupId: string, concurrencyLimit: number): Promise<SandboxGroup> {
    return unwrap(
      await this.apiClient.PATCH("/sandbox-groups/{sandboxGroupId}", {
        params: { path: { sandboxGroupId } },
        body: { concurrencyLimit },
      }),
      "Failed to update sandbox group",
    );
  }

  /**
   * Deletes a group and terminates its sandboxes. Its snapshots and credentials are deleted
   * shortly after. Throws `SandboxGroupDefaultNotDeletableError` for the workspace's default
   * group (make another group the default first with `setDefaultGroup()`) and
   * `SandboxGroupSuspendedError` for a suspended group.
   */
  async deleteGroup(sandboxGroupId: string): Promise<void> {
    const { error, response } = await this.apiClient.DELETE("/sandbox-groups/{sandboxGroupId}", {
      params: { path: { sandboxGroupId } },
    });
    if (error !== undefined || !response.ok) {
      throw getTypedApiError(error, response, "Failed to delete sandbox group");
    }
  }

  /**
   * Makes a group the workspace's default. Setting the current default returns it unchanged.
   * Throws `SandboxGroupSuspendedError` for a suspended group.
   */
  async setDefaultGroup(sandboxGroupId: string): Promise<SandboxGroup> {
    return unwrap(
      await this.apiClient.POST("/sandbox-groups/{sandboxGroupId}/set-default", {
        params: { path: { sandboxGroupId } },
      }),
      "Failed to set default sandbox group",
      getTypedApiError,
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
    signalOrOptions?: AbortSignal | SandboxDownloadOptions,
  ): Promise<SandboxDownload> {
    const { signal, maxSizeBytes } = toDownloadOptions(signalOrOptions);
    const limit = downloadLimit(sandboxId, path, maxSizeBytes, DEFAULT_DOWNLOAD_MAX_BYTES);

    return this.fetchDownload(sandboxId, path, ownerId, signal, async (response) => {
      const data = await readLimitedBody(response, limit);

      return {
        data,
        size: data.byteLength,
        contentType: response.headers.get("Content-Type") ?? undefined,
      };
    });
  }

  /**
   * Streams a local file to a path in the sandbox without holding it in memory. Directories
   * can't be copied this way.
   */
  async copyTo(
    sandboxId: string,
    { localPath, remotePath, ownerId, signal }: SandboxCopyToOptions,
  ): Promise<void> {
    if (signal?.aborted) {
      throw new AbortError();
    }

    const source = await stat(localPath);
    if (!source.isFile()) {
      throw new RenderError(`${localPath} is not a regular file; copyTo copies only files`);
    }

    const tokenResponse = await this.getFileConnectToken(sandboxId, remotePath, "upload", ownerId);
    await putFile(tokenResponse, localPath, source.size, signal);
  }

  /**
   * Streams a sandbox file to a local path without holding it in memory. An existing file is
   * replaced. Directories can't be copied this way. A failed local write throws
   * `SandboxDownloadError`.
   */
  async copyFrom(
    sandboxId: string,
    { remotePath, localPath, ownerId, signal, maxSizeBytes }: SandboxCopyFromOptions,
  ): Promise<SandboxCopyFromResult> {
    const limit = downloadLimit(sandboxId, remotePath, maxSizeBytes, Number.POSITIVE_INFINITY);

    return this.fetchDownload(sandboxId, remotePath, ownerId, signal, (response) =>
      saveLimitedBody(response, localPath, limit),
    );
  }

  private async fetchDownload<T>(
    sandboxId: string,
    path: string,
    ownerId: `tea-${string}` | undefined,
    signal: AbortSignal | undefined,
    read: (response: Response) => Promise<T>,
  ): Promise<T> {
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

      return await read(response);
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
   * The connect token endpoint returns a 409 `sandbox_not_running` for a sandbox that has
   * ended. Older API versions returned a bare 404, which also means a sandbox that isn't ready
   * yet. Look up the sandbox to name its status and end time.
   */
  private async explainEndedSandbox(
    err: unknown,
    sandboxId: string,
    ownerId: `tea-${string}` | undefined,
    context: string,
  ): Promise<unknown> {
    if (
      !(err instanceof ClientError) ||
      !(err.statusCode === 404 || (err.statusCode === 409 && err.code === "sandbox_not_running"))
    ) {
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

    const tokenResponse = await this.getRunConnectToken(sandboxId, "stream", ownerId);

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

/**
 * The API sends a credential 404 without a code, and the same 404 for a missing sandbox group, so
 * only calls whose path names a credential use this.
 */
function getCredentialApiError(error: unknown, response: Response, context: string): Error {
  const apiError = getTypedApiError(error, response, context);
  if (apiError instanceof ClientError && apiError.statusCode === 404) {
    return new SandboxCredentialNotFoundError(
      apiError.message,
      apiError.statusCode,
      apiError.response,
      apiError.code,
    );
  }
  return apiError;
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
