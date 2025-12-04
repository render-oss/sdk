import type { Client } from 'openapi-fetch';
import { ClientError, ServerError } from './errors.js';
import type { paths } from './schema.js';
import type { SSEClient } from './sse.js';
import type {
  ListTaskRunsParams,
  TaskData,
  TaskIdentifier,
  TaskRun,
  TaskRunDetails,
} from './types.js';

/**
 * Helper function to handle API errors and throw appropriate custom error types
 */
function handleApiError(error: any, response: Response, context: string): never {
  const statusCode = response.status;
  const errorMessage = `${context}: ${error}`;

  if (statusCode >= 500) {
    throw new ServerError(errorMessage, statusCode, error);
  } else if (statusCode >= 400) {
    throw new ClientError(errorMessage, statusCode, error);
  }
  throw new ClientError(errorMessage, statusCode, error);
}

/**
 * Workflows service for managing task runs
 */
export class WorkflowsService {
  constructor(
    private sseClient: SSEClient,
    private apiClient: Client<paths>
  ) {}

  /**
   * Run a task and return an awaitable task run
   * @param taskIdentifier Task identifier in the format "workflow-slug/task-name"
   * @param inputData Input data as an array of parameters
   * @returns Awaitable task run
   */
  async runTask(taskIdentifier: TaskIdentifier, inputData: TaskData): Promise<TaskRun> {
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

  async waitForTask(taskRunId: string): Promise<TaskRunDetails> {
    return this.sseClient.waitOnTaskRun(taskRunId);
  }

  /**
   * Get task run details by ID
   * @param taskRunId Task run ID
   * @returns Task run details
   */

  async getTaskRun(taskRunId: string): Promise<TaskRunDetails> {
    const { data, error, response } = await this.apiClient.GET('/task-runs/{taskRunId}', {
      params: { path: { taskRunId } },
    });
    if (error) {
      handleApiError(error, response, 'Failed to get task run');
    }
    return data;
  }

  /**
   * Cancel a task run
   * @param taskRunId Task run ID
   */

  async cancelTaskRun(taskRunId: string): Promise<void> {
    const { error, response } = await this.apiClient.DELETE('/task-runs/{taskRunId}', {
      params: { path: { taskRunId } },
    });
    if (error) {
      handleApiError(error, response, 'Failed to cancel task run');
    }
  }

  /**
   * List task runs with optional filters
   * @param params Filter parameters
   * @returns List of task runs
   */

  async listTaskRuns(params: ListTaskRunsParams): Promise<TaskRun[]> {
    const { data, error, response } = await this.apiClient.GET('/task-runs', {
      params: { query: params },
    });
    if (error) {
      handleApiError(error, response, 'Failed to list task runs');
    }
    return data;
  }
}
