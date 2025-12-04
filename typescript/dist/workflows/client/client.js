"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Client = void 0;
const openapi_fetch_1 = __importDefault(require("openapi-fetch"));
const errors_js_1 = require("./errors.js");
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
class Client {
    constructor(options) {
        let baseUrl;
        const useLocalDev = options?.useLocalDev ?? process.env.RENDER_USE_LOCAL_DEV === 'true';
        if (useLocalDev) {
            baseUrl = options?.localDevUrl || process.env.RENDER_LOCAL_DEV_URL || 'http://localhost:8120';
        }
        else {
            baseUrl = options?.baseUrl || 'https://api.render.com';
        }
        const token = options?.token || process.env.RENDER_API_KEY;
        if (!token) {
            throw new errors_js_1.RenderError('API token is required. Provide it via options.token or RENDER_API_KEY environment variable.');
        }
        this.sse = new sse_js_1.SSEClient(baseUrl, token);
        this.apiClient = (0, openapi_fetch_1.default)({
            baseUrl: `${baseUrl}/v1`,
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
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
            signal?.addEventListener('abort', abortHandler);
            const { data, error, response } = await this.apiClient.POST('/task-runs', {
                body: {
                    task: taskIdentifier,
                    input: inputData,
                },
                signal,
            });
            if (error) {
                handleApiError(error, response, 'Failed to run task');
            }
            taskRunId = data.id;
            return await this.waitForTask(data.id, signal);
        }
        catch (err) {
            if (err instanceof DOMException && err.name === 'AbortError') {
                throw new errors_js_1.AbortError();
            }
            throw err;
        }
        finally {
            signal?.removeEventListener('abort', abortHandler);
        }
    }
    async waitForTask(taskRunId, signal) {
        return this.sse.waitOnTaskRun(taskRunId, signal);
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
exports.Client = Client;
