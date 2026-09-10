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
 * Error for HTTP server errors (5xx)
 */
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

export class AbortError extends Error {
  constructor() {
    super("The operation was aborted.");
    this.name = "AbortError";
  }
}
