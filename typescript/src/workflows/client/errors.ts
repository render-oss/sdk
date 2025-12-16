/**
 * Base error class for all Render SDK errors
 */
export class RenderError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'RenderError';
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
    public taskError?: string
  ) {
    super(message);
    this.name = 'TaskRunError';
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
    public response?: any
  ) {
    super(message);
    this.name = 'ClientError';
    Object.setPrototypeOf(this, ClientError.prototype);
  }
}

/**
 * Error for HTTP server errors (5xx)
 */
export class ServerError extends RenderError {
  constructor(
    message: string,
    public statusCode: number,
    public response?: any
  ) {
    super(message);
    this.name = 'ServerError';
    Object.setPrototypeOf(this, ServerError.prototype);
  }
}

/**
 * Error for request timeouts
 */
export class TimeoutError extends RenderError {
  constructor(message: string) {
    super(message);
    this.name = 'TimeoutError';
    Object.setPrototypeOf(this, TimeoutError.prototype);
  }
}

export class AbortError extends Error {
  constructor() {
    super('The operation was aborted.');
    this.name = 'AbortError';
  }
}
