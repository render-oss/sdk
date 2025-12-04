export declare class TaskExecutor {
    private udsClient;
    private context;
    constructor(socketPath: string);
    executeTask(): Promise<void>;
    registerTasks(): Promise<void>;
}
//# sourceMappingURL=executor.d.ts.map