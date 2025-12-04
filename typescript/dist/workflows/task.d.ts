import type { RegisterTaskOptions, TaskContext, TaskFunction } from './types.js';
export declare function getCurrentContext(): TaskContext | undefined;
export declare function setCurrentContext<T>(context: TaskContext, fn: () => Promise<T>): Promise<T>;
export declare function task<TArgs extends any[], TResult>(options: RegisterTaskOptions, func: TaskFunction<TArgs, TResult>): TaskFunction<TArgs, TResult>;
//# sourceMappingURL=task.d.ts.map