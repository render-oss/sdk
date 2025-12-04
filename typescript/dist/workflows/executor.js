"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TaskExecutor = void 0;
const errors_js_1 = require("./client/errors.js");
const registry_js_1 = require("./registry.js");
const task_js_1 = require("./task.js");
const uds_js_1 = require("./uds.js");
class TaskResultImpl {
    constructor(subtaskId, udsClient) {
        this.subtaskId = subtaskId;
        this.udsClient = udsClient;
    }
    async get() {
        const maxAttempts = 120;
        const pollInterval = 500;
        for (let i = 0; i < maxAttempts; i++) {
            const result = await this.udsClient.getSubtaskResult(this.subtaskId);
            if (!result.still_running && result.complete) {
                if (result.complete.output) {
                    const json = Buffer.from(result.complete.output, 'base64').toString();
                    const decoded = JSON.parse(json);
                    return decoded[0];
                }
                return undefined;
            }
            else if (!result.still_running && result.error) {
                throw new errors_js_1.RenderError(`Subtask failed: ${result.error}`);
            }
            await new Promise((resolve) => setTimeout(resolve, pollInterval));
        }
        throw new errors_js_1.RenderError('Subtask did not complete within timeout');
    }
}
class TaskContextImpl {
    constructor(udsClient) {
        this.udsClient = udsClient;
    }
    executeTask(_task, taskName, ...args) {
        const registry = registry_js_1.TaskRegistry.getInstance();
        if (!registry.has(taskName)) {
            throw new errors_js_1.RenderError(`Task '${taskName}' is not registered`);
        }
        const subtaskIdPromise = this.udsClient.runSubtask(taskName, args);
        return {
            get: async () => {
                const subtaskId = await subtaskIdPromise;
                const result = new TaskResultImpl(subtaskId, this.udsClient);
                return result.get();
            },
        };
    }
}
class TaskExecutor {
    constructor(socketPath) {
        this.udsClient = new uds_js_1.UDSClient(socketPath);
        this.context = new TaskContextImpl(this.udsClient);
    }
    async executeTask() {
        const registry = registry_js_1.TaskRegistry.getInstance();
        try {
            const input = await this.udsClient.getInput();
            const taskName = input.task_name;
            const inputData = JSON.parse(Buffer.from(input.input, 'base64').toString());
            const taskMetadata = registry.get(taskName);
            if (!taskMetadata) {
                throw new errors_js_1.RenderError(`Task '${taskName}' not found in registry`);
            }
            const result = await (0, task_js_1.setCurrentContext)(this.context, async () => {
                return await taskMetadata.func(...inputData);
            });
            await this.udsClient.sendCallback(result);
        }
        catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            await this.udsClient.sendCallback(undefined, errorMessage);
            throw error;
        }
    }
    async registerTasks() {
        const registry = registry_js_1.TaskRegistry.getInstance();
        const tasks = registry.getAllTasks();
        await this.udsClient.registerTasks(tasks);
    }
}
exports.TaskExecutor = TaskExecutor;
