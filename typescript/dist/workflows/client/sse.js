"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SSEClient = exports.TaskEventType = void 0;
const eventsource_1 = require("eventsource");
const errors_js_1 = require("./errors.js");
var TaskEventType;
(function (TaskEventType) {
    TaskEventType["COMPLETED"] = "task.completed";
    TaskEventType["FAILED"] = "task.failed";
    TaskEventType["RUNNING"] = "task.running";
    TaskEventType["PENDING"] = "task.pending";
})(TaskEventType || (exports.TaskEventType = TaskEventType = {}));
class SSEClient {
    constructor(baseUrl, token) {
        this.baseUrl = baseUrl;
        this.token = token;
    }
    async waitOnTaskRun(taskRunId, signal) {
        return new Promise((resolve, reject) => {
            let eventSource = null;
            const abortHandler = () => {
                cleanup();
                reject(new errors_js_1.AbortError());
            };
            const cleanup = () => {
                if (eventSource) {
                    eventSource.removeEventListener(TaskEventType.COMPLETED, eventHandler);
                    eventSource.removeEventListener(TaskEventType.FAILED, eventHandler);
                    eventSource.removeEventListener('error', errorHandler);
                    eventSource.close();
                    eventSource = null;
                }
                signal?.removeEventListener('abort', abortHandler);
            };
            const eventHandler = (event) => {
                try {
                    const details = JSON.parse(event.data);
                    cleanup();
                    resolve(details);
                }
                catch (e) {
                    cleanup();
                    reject(new Error(`Failed to parse task run details: ${e}`));
                }
            };
            const errorHandler = (error) => {
                cleanup();
                reject(new Error(`SSE connection error: ${error.message || 'Unknown error'}`));
            };
            if (signal?.aborted) {
                reject(new errors_js_1.AbortError());
                return;
            }
            signal?.addEventListener('abort', abortHandler);
            try {
                const url = new URL('/v1/task-runs/events', this.baseUrl);
                url.searchParams.append('taskRunIds', taskRunId);
                eventSource = new eventsource_1.EventSource(url.toString(), {
                    fetch: (input, init) => fetch(input, {
                        ...init,
                        headers: {
                            ...init?.headers,
                            Authorization: `Bearer ${this.token}`,
                        },
                    }),
                });
                eventSource.addEventListener(TaskEventType.COMPLETED, eventHandler);
                eventSource.addEventListener(TaskEventType.FAILED, eventHandler);
                eventSource.addEventListener('error', errorHandler);
            }
            catch (e) {
                cleanup();
                reject(e);
            }
        });
    }
}
exports.SSEClient = SSEClient;
