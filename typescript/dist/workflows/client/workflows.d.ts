import type { Client } from 'openapi-fetch';
import type { paths } from './schema.js';
import type { SSEClient } from './sse.js';
import type { ListTaskRunsParams, TaskData, TaskIdentifier, TaskRun, TaskRunDetails } from './types.js';
export declare class WorkflowsService {
    private sseClient;
    private apiClient;
    constructor(sseClient: SSEClient, apiClient: Client<paths>);
    runTask(taskIdentifier: TaskIdentifier, inputData: TaskData): Promise<TaskRun>;
    waitForTask(taskRunId: string): Promise<TaskRunDetails>;
    getTaskRun(taskRunId: string): Promise<TaskRunDetails>;
    cancelTaskRun(taskRunId: string): Promise<void>;
    listTaskRuns(params: ListTaskRunsParams): Promise<TaskRun[]>;
}
//# sourceMappingURL=workflows.d.ts.map