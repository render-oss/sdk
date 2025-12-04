import { type Client as ApiClient } from 'openapi-fetch';
import type { paths } from './schema.js';
import { SSEClient } from './sse.js';
import type { ClientOptions, ListTaskRunsParams, TaskData, TaskIdentifier, TaskRun, TaskRunDetails } from './types.js';
export declare class Client {
    readonly sse: SSEClient;
    readonly apiClient: ApiClient<paths>;
    constructor(options?: ClientOptions);
    runTask(taskIdentifier: TaskIdentifier, inputData: TaskData, signal?: AbortSignal): Promise<TaskRunDetails>;
    private waitForTask;
    getTaskRun(taskRunId: string): Promise<TaskRunDetails>;
    private cancelTaskRun;
    listTaskRuns(params: ListTaskRunsParams): Promise<TaskRun[]>;
}
//# sourceMappingURL=client.d.ts.map