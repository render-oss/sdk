"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WorkflowsClient = void 0;
const errors_js_1 = require("../../errors.js");
const sse_js_1 = require("./sse.js");
function handleApiError(error, response, context) {
    const statusCode = response.status;
    const errorMessage = `${context}: ${error}`;
    if (statusCode >= 500) {
        throw new errors_js_1.ServerError(errorMessage, statusCode, error);
    }
    else if (statusCode >= 400) {
        throw new errors_js_1.ClientError(errorMessage, statusCode, error);
    }
    throw new errors_js_1.ClientError(errorMessage, statusCode, error);
}
class WorkflowsClient {
    constructor(apiClient, baseUrl, token) {
        this.sse = new sse_js_1.SSEClient(baseUrl, token);
        this.apiClient = apiClient;
    }
    async runTask(taskIdentifier, inputData, signal) {
        if (signal?.aborted) {
            throw new errors_js_1.AbortError();
        }
        let taskRunId = null;
        const abortHandler = async () => {
            if (taskRunId) {
                await this.cancelTaskRun(taskRunId);
                throw new errors_js_1.AbortError();
            }
        };
        try {
            signal?.addEventListener("abort", abortHandler);
            const { data, error, response } = await this.apiClient.POST("/task-runs", {
                body: {
                    task: taskIdentifier,
                    input: inputData,
                },
                signal,
            });
            if (error) {
                handleApiError(error, response, "Failed to run task");
            }
            taskRunId = data.id;
            return await this.waitForTask(data.id, signal);
        }
        catch (err) {
            if (err instanceof DOMException && err.name === "AbortError") {
                throw new errors_js_1.AbortError();
            }
            throw err;
        }
        finally {
            signal?.removeEventListener("abort", abortHandler);
        }
    }
    async waitForTask(taskRunId, signal) {
        return this.sse.waitOnTaskRun(taskRunId, signal);
    }
    async getTaskRun(taskRunId) {
        const { data, error, response } = await this.apiClient.GET("/task-runs/{taskRunId}", {
            params: { path: { taskRunId } },
        });
        if (error) {
            handleApiError(error, response, "Failed to get task run");
        }
        return data;
    }
    async cancelTaskRun(taskRunId) {
        const { error, response } = await this.apiClient.DELETE("/task-runs/{taskRunId}", {
            params: { path: { taskRunId } },
        });
        if (error) {
            handleApiError(error, response, "Failed to cancel task run");
        }
    }
    async listTaskRuns(params) {
        const { data, error, response } = await this.apiClient.GET("/task-runs", {
            params: { query: params },
        });
        if (error) {
            handleApiError(error, response, "Failed to list task runs");
        }
        return data;
    }
}
exports.WorkflowsClient = WorkflowsClient;
