import type { RegisterTaskOptions, TaskFunction, TaskMetadata } from './types.js';
export declare class TaskRegistry {
    private static instance;
    private tasks;
    private constructor();
    static getInstance(): TaskRegistry;
    register(func: TaskFunction, options: RegisterTaskOptions): void;
    get(name: string): TaskMetadata | undefined;
    getAllTaskNames(): string[];
    getAllTasks(): TaskMetadata[];
    has(name: string): boolean;
    clear(): void;
}
//# sourceMappingURL=registry.d.ts.map