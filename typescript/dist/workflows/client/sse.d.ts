import type { TaskRunDetails } from './types.js';
export declare enum TaskEventType {
    COMPLETED = "task.completed",
    FAILED = "task.failed",
    RUNNING = "task.running",
    PENDING = "task.pending"
}
export declare class SSEClient {
    private baseUrl;
    private token;
    constructor(baseUrl: string, token: string);
    waitOnTaskRun(taskRunId: string, signal?: AbortSignal): Promise<TaskRunDetails>;
}
//# sourceMappingURL=sse.d.ts.map