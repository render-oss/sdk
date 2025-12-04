import type { GetInputResponse, GetSubtaskResultResponse, TaskMetadata } from './types.js';
export declare class UDSClient {
    private socketPath;
    constructor(socketPath: string);
    getInput(): Promise<GetInputResponse>;
    private buildCallbackBody;
    sendCallback(results?: any, error?: string): Promise<void>;
    runSubtask(taskName: string, input: any[]): Promise<string>;
    getSubtaskResult(subtaskId: string): Promise<GetSubtaskResultResponse>;
    registerTasks(tasks: TaskMetadata[]): Promise<void>;
    private request;
}
//# sourceMappingURL=uds.d.ts.map