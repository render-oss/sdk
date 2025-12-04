export declare class RenderError extends Error {
    constructor(message: string);
}
export declare class TaskRunError extends RenderError {
    taskRunId?: string | undefined;
    taskError?: string | undefined;
    constructor(message: string, taskRunId?: string | undefined, taskError?: string | undefined);
}
export declare class ClientError extends RenderError {
    statusCode: number;
    response?: any | undefined;
    constructor(message: string, statusCode: number, response?: any | undefined);
}
export declare class ServerError extends RenderError {
    statusCode: number;
    response?: any | undefined;
    constructor(message: string, statusCode: number, response?: any | undefined);
}
export declare class TimeoutError extends RenderError {
    constructor(message: string);
}
export declare class AbortError extends Error {
    constructor();
}
//# sourceMappingURL=errors.d.ts.map