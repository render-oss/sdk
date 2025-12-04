"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TaskRegistry = void 0;
class TaskRegistry {
    constructor() {
        this.tasks = new Map();
    }
    static getInstance() {
        if (!TaskRegistry.instance) {
            TaskRegistry.instance = new TaskRegistry();
        }
        return TaskRegistry.instance;
    }
    register(func, options) {
        const taskName = options.name;
        if (!taskName) {
            throw new Error('Task function must have a name or name must be provided');
        }
        let taskOptions;
        if (options.retry) {
            taskOptions = {
                retry: {
                    max_retries: options.retry.maxRetries,
                    wait_duration_ms: options.retry.maxRetries,
                    factor: options.retry.factor,
                },
            };
        }
        this.tasks.set(taskName, {
            name: taskName,
            func,
            options: taskOptions,
        });
    }
    get(name) {
        return this.tasks.get(name);
    }
    getAllTaskNames() {
        return Array.from(this.tasks.keys());
    }
    getAllTasks() {
        return Array.from(this.tasks.values());
    }
    has(name) {
        return this.tasks.has(name);
    }
    clear() {
        this.tasks.clear();
    }
}
exports.TaskRegistry = TaskRegistry;
