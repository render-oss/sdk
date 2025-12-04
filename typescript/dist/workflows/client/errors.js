"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AbortError = exports.TimeoutError = exports.ServerError = exports.ClientError = exports.TaskRunError = exports.RenderError = void 0;
class RenderError extends Error {
    constructor(message) {
        super(message);
        this.name = 'RenderError';
        Object.setPrototypeOf(this, RenderError.prototype);
    }
}
exports.RenderError = RenderError;
class TaskRunError extends RenderError {
    constructor(message, taskRunId, taskError) {
        super(message);
        this.taskRunId = taskRunId;
        this.taskError = taskError;
        this.name = 'TaskRunError';
        Object.setPrototypeOf(this, TaskRunError.prototype);
    }
}
exports.TaskRunError = TaskRunError;
class ClientError extends RenderError {
    constructor(message, statusCode, response) {
        super(message);
        this.statusCode = statusCode;
        this.response = response;
        this.name = 'ClientError';
        Object.setPrototypeOf(this, ClientError.prototype);
    }
}
exports.ClientError = ClientError;
class ServerError extends RenderError {
    constructor(message, statusCode, response) {
        super(message);
        this.statusCode = statusCode;
        this.response = response;
        this.name = 'ServerError';
        Object.setPrototypeOf(this, ServerError.prototype);
    }
}
exports.ServerError = ServerError;
class TimeoutError extends RenderError {
    constructor(message) {
        super(message);
        this.name = 'TimeoutError';
        Object.setPrototypeOf(this, TimeoutError.prototype);
    }
}
exports.TimeoutError = TimeoutError;
class AbortError extends Error {
    constructor() {
        super('The operation was aborted.');
        this.name = 'AbortError';
    }
}
exports.AbortError = AbortError;
