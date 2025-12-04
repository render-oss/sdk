import type { components } from './schema.js';
export type TaskFunction<TArgs extends any[] = any[], TResult = any> = (...args: TArgs) => TResult | Promise<TResult>;
export type TaskOptions = components['schemas']['TaskOptions'];
export interface TaskMetadata {
    name: string;
    func: TaskFunction;
    options?: TaskOptions;
}
export interface TaskContext {
    executeTask<TArgs extends any[], TResult>(task: TaskFunction<TArgs, TResult>, taskName: string, ...args: TArgs): TaskResult<TResult>;
}
export interface TaskResult<T> {
    get(): Promise<T>;
}
export interface TaskInput {
    task_name: string;
    input: any[];
}
export type CallbackRequest = components['schemas']['CallbackRequest'];
export type GetInputResponse = components['schemas']['InputResponse'];
export type RunSubtaskRequest = components['schemas']['RunSubtaskRequest'];
export type RunSubtaskResponse = components['schemas']['RunSubtaskResponse'];
export type GetSubtaskResultRequest = components['schemas']['SubtaskResultRequest'];
export type GetSubtaskResultResponse = components['schemas']['SubtaskResultResponse'];
export type RegisterTasksRequest = components['schemas']['Tasks'];
export interface Retry {
    maxRetries: number;
    waitDurationMs: number;
    factor?: number;
}
export interface RegisterTaskOptions {
    retry?: Retry;
    name: string;
}
//# sourceMappingURL=types.d.ts.map