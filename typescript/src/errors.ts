/**
 * Base error class for all Render SDK errors
 */
export class RenderError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "RenderError";
    Object.setPrototypeOf(this, RenderError.prototype);
  }
}

/**
 * Error for task execution failures
 */
export class TaskRunError extends RenderError {
  constructor(
    message: string,
    public taskRunId?: string,
    public taskError?: string,
  ) {
    super(message);
    this.name = "TaskRunError";
    Object.setPrototypeOf(this, TaskRunError.prototype);
  }
}

/**
 * Error for HTTP client errors (4xx)
 */
export class ClientError extends RenderError {
  constructor(
    message: string,
    public statusCode: number,
    public response?: any,
    public code?: string,
  ) {
    super(message);
    this.name = "ClientError";
    Object.setPrototypeOf(this, ClientError.prototype);
  }
}

/**
 * The snapshot does not exist, is deleted or expired, or belongs to another sandbox group
 */
export class SandboxSnapshotNotFoundError extends ClientError {
  constructor(message: string, statusCode: number, response?: any, code?: string) {
    super(message, statusCode, response, code);
    this.name = "SandboxSnapshotNotFoundError";
    Object.setPrototypeOf(this, SandboxSnapshotNotFoundError.prototype);
  }
}

/**
 * The sandbox has ended (`terminated` or `errored`), for example because it passed its timeout.
 * It can't run commands or transfer files, so retrying won't help.
 */
export class SandboxEndedError extends ClientError {
  constructor(
    message: string,
    statusCode: number,
    public sandboxStatus: "terminated" | "errored",
    response?: any,
    code?: string,
  ) {
    super(message, statusCode, response, code);
    this.name = "SandboxEndedError";
    Object.setPrototypeOf(this, SandboxEndedError.prototype);
  }
}

/**
 * The snapshot is not `available`: its capture is still in progress or has failed
 */
export class SandboxSnapshotNotReadyError extends ClientError {
  constructor(message: string, statusCode: number, response?: any, code?: string) {
    super(message, statusCode, response, code);
    this.name = "SandboxSnapshotNotReadyError";
    Object.setPrototypeOf(this, SandboxSnapshotNotReadyError.prototype);
  }
}

/**
 * A `runtime` snapshot was restored onto a different `plan` than its source sandbox
 */
export class SandboxSnapshotPlanMismatchError extends ClientError {
  constructor(message: string, statusCode: number, response?: any, code?: string) {
    super(message, statusCode, response, code);
    this.name = "SandboxSnapshotPlanMismatchError";
    Object.setPrototypeOf(this, SandboxSnapshotPlanMismatchError.prototype);
  }
}

/**
 * No image in the sandbox group has the requested ID or name
 */
export class SandboxImageNotFoundError extends ClientError {
  constructor(message: string, statusCode: number, response?: any, code?: string) {
    super(message, statusCode, response, code);
    this.name = "SandboxImageNotFoundError";
    Object.setPrototypeOf(this, SandboxImageNotFoundError.prototype);
  }
}

/**
 * The image has not `succeeded`: it is still `pending` or `running`, or it `failed`
 */
export class SandboxImageNotReadyError extends ClientError {
  constructor(message: string, statusCode: number, response?: any, code?: string) {
    super(message, statusCode, response, code);
    this.name = "SandboxImageNotReadyError";
    Object.setPrototypeOf(this, SandboxImageNotReadyError.prototype);
  }
}

/** @deprecated Use `SandboxImageNotFoundError`. */
export const SandboxBuildNotFoundError = SandboxImageNotFoundError;
/** @deprecated Use `SandboxImageNotFoundError`. */
export type SandboxBuildNotFoundError = SandboxImageNotFoundError;

/** @deprecated Use `SandboxImageNotReadyError`. */
export const SandboxBuildNotReadyError = SandboxImageNotReadyError;
/** @deprecated Use `SandboxImageNotReadyError`. */
export type SandboxBuildNotReadyError = SandboxImageNotReadyError;

/**
 * While waiting for the sandbox to be `running`, it reached a status it can't run from:
 * `errored`, `terminated`, `suspending`, or `suspended`. The sandbox is left as it is.
 */
export class SandboxNotRunningError extends RenderError {
  constructor(
    message: string,
    public sandboxId: string,
    public sandboxStatus: string,
  ) {
    super(message);
    this.name = "SandboxNotRunningError";
    Object.setPrototypeOf(this, SandboxNotRunningError.prototype);
  }
}

/**
 * While waiting for the snapshot to be `available`, its capture failed
 */
export class SandboxSnapshotFailedError extends RenderError {
  constructor(
    message: string,
    public snapshotId: string,
    public snapshotError?: string,
  ) {
    super(message);
    this.name = "SandboxSnapshotFailedError";
    Object.setPrototypeOf(this, SandboxSnapshotFailedError.prototype);
  }
}

/**
 * Error for HTTP server errors (5xx)
 */
/**
 * While waiting for the image to be ready, its import failed. `failureReason` is the reason the
 * API reports, if any.
 */
export class SandboxImageFailedError extends RenderError {
  constructor(
    message: string,
    public imageId: string,
    public failureReason?: string,
  ) {
    super(message);
    this.name = "SandboxImageFailedError";
    Object.setPrototypeOf(this, SandboxImageFailedError.prototype);
  }
}

export class ServerError extends RenderError {
  constructor(
    message: string,
    public statusCode: number,
    public response?: any,
  ) {
    super(message);
    this.name = "ServerError";
    Object.setPrototypeOf(this, ServerError.prototype);
  }
}

/**
 * Error for request timeouts
 */
export class TimeoutError extends RenderError {
  constructor(message: string) {
    super(message);
    this.name = "TimeoutError";
    Object.setPrototypeOf(this, TimeoutError.prototype);
  }
}

/**
 * The sandbox was not `running` before the wait timed out. The sandbox is left as it is and may
 * still become `running`. `lastStatus` is unset if no status check finished in time.
 */
export class SandboxWaitTimeoutError extends TimeoutError {
  constructor(
    message: string,
    public sandboxId: string,
    public timeoutMs: number,
    public lastStatus?: string,
  ) {
    super(message);
    this.name = "SandboxWaitTimeoutError";
    Object.setPrototypeOf(this, SandboxWaitTimeoutError.prototype);
  }
}

/**
 * The image did not succeed before the wait timed out. The import keeps running and may still
 * succeed. `lastStatus` is unset if no status check finished in time.
 */
export class SandboxImageWaitTimeoutError extends TimeoutError {
  constructor(
    message: string,
    public imageId: string,
    public timeoutMs: number,
    public lastStatus?: string,
  ) {
    super(message);
    this.name = "SandboxImageWaitTimeoutError";
    Object.setPrototypeOf(this, SandboxImageWaitTimeoutError.prototype);
  }
}

/**
 * The snapshot was not `available` before the wait timed out. It may still become `available`.
 * `lastStatus` is unset if no status check finished in time.
 */
export class SandboxSnapshotWaitTimeoutError extends TimeoutError {
  constructor(
    message: string,
    public snapshotId: string,
    public timeoutMs: number,
    public lastStatus?: string,
  ) {
    super(message);
    this.name = "SandboxSnapshotWaitTimeoutError";
    Object.setPrototypeOf(this, SandboxSnapshotWaitTimeoutError.prototype);
  }
}

/**
 * `create({ wait })` created the sandbox, but the wait for it to be `running` failed. The sandbox
 * still exists and is billed until it ends, so call `terminate(sandboxId)` if you don't want it.
 * `cause` is the error the wait threw, such as `SandboxNotRunningError`,
 * `SandboxWaitTimeoutError`, `AbortError`, or a request error.
 */
export class SandboxCreateWaitError extends RenderError {
  constructor(
    message: string,
    public sandboxId: string,
    public cause: unknown,
  ) {
    super(message);
    this.name = "SandboxCreateWaitError";
    Object.setPrototypeOf(this, SandboxCreateWaitError.prototype);
  }
}

/**
 * `snapshots.create({ wait })` created the snapshot, but the wait for it to be `available`
 * failed. The snapshot still exists, so delete it with `sandboxGroupId` and `snapshotId` if you
 * don't want it. Deleting fails with `SandboxSnapshotNotReadyError` while the capture is still
 * running. `cause` is the error the wait threw, such as `SandboxSnapshotFailedError`,
 * `SandboxSnapshotWaitTimeoutError`, `AbortError`, or a request error.
 */
export class SandboxSnapshotCreateWaitError extends RenderError {
  constructor(
    message: string,
    public snapshotId: string,
    public sandboxGroupId: string,
    public cause: unknown,
  ) {
    super(message);
    this.name = "SandboxSnapshotCreateWaitError";
    Object.setPrototypeOf(this, SandboxSnapshotCreateWaitError.prototype);
  }
}

export class AbortError extends Error {
  constructor() {
    super("The operation was aborted.");
    this.name = "AbortError";
  }
}
