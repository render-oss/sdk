import type { components, paths } from './schema';
export type TaskIdentifier = string;
export type TaskData = Array<any>;
export declare enum TaskRunStatus {
    PENDING = "pending",
    RUNNING = "running",
    COMPLETED = "completed",
    FAILED = "failed"
}
export type TaskRun = components['schemas']['TaskRun'];
export type TaskRunDetails = components['schemas']['TaskRunDetails'];
export type ListTaskRunsParams = paths['/task-runs']['get']['parameters']['query'];
export interface RunTaskRequest {
    task: TaskIdentifier;
    input: TaskData;
}
export interface ClientOptions {
    token?: string;
    baseUrl?: string;
    useLocalDev?: boolean;
    localDevUrl?: string;
}
//# sourceMappingURL=types.d.ts.map