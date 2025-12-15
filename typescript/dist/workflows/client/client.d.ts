import type { Client as ApiClient } from "openapi-fetch";
import type { paths } from "../../utils/schema.js";
import type { ListTaskRunsParams, TaskData, TaskIdentifier, TaskRun, TaskRunDetails } from "./types.js";
export declare class WorkflowsClient {
    private readonly sse;
    private readonly apiClient;
    constructor(apiClient: ApiClient<paths>, baseUrl: string, token: string);
    runTask(taskIdentifier: TaskIdentifier, inputData: TaskData, signal?: AbortSignal): Promise<TaskRunDetails>;
    private waitForTask;
    getTaskRun(taskRunId: string): Promise<TaskRunDetails>;
    private cancelTaskRun;
    listTaskRuns(params: ListTaskRunsParams): Promise<TaskRun[]>;
}
//# sourceMappingURL=client.d.ts.map