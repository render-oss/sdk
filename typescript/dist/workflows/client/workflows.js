"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WorkflowsService = void 0;
const errors_js_1 = require("./errors.js");
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
class WorkflowsService {
    constructor(sseClient, apiClient) {
        this.sseClient = sseClient;
        this.apiClient = apiClient;
    }
    async runTask(taskIdentifier, inputData) {
        const { data, error, response } = await this.apiClient.POST('/task-runs', {
            body: {
                task: taskIdentifier,
                input: inputData,
            },
        });
        if (error) {
            handleApiError(error, response, 'Failed to run task');
        }
        return data;
    }
    async waitForTask(taskRunId) {
        return this.sseClient.waitOnTaskRun(taskRunId);
    }
    async getTaskRun(taskRunId) {
        const { data, error, response } = await this.apiClient.GET('/task-runs/{taskRunId}', {
            params: { path: { taskRunId } },
        });
        if (error) {
            handleApiError(error, response, 'Failed to get task run');
        }
        return data;
    }
    async cancelTaskRun(taskRunId) {
        const { error, response } = await this.apiClient.DELETE('/task-runs/{taskRunId}', {
            params: { path: { taskRunId } },
        });
        if (error) {
            handleApiError(error, response, 'Failed to cancel task run');
        }
    }
    async listTaskRuns(params) {
        const { data, error, response } = await this.apiClient.GET('/task-runs', {
            params: { query: params },
        });
        if (error) {
            handleApiError(error, response, 'Failed to list task runs');
        }
        return data;
    }
}
exports.WorkflowsService = WorkflowsService;
