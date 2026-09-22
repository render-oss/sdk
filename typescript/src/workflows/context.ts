import { RenderError } from "../errors.js";
import { TaskRegistry } from "./registry.js";
import type { GetInputResponse, TaskContext, TaskDefinition, TaskRunMetadata } from "./types.js";
import type { UDSClient } from "./uds.js";

const SUBTASK_POLL_INTERVAL_MS = 500;

/**
 * The {@link TaskContext} handed to tasks running under the workflow system.
 *
 * Each run is submitted over the Unix domain socket and polled to
 * completion.
 */
export class WorkflowTaskContext implements TaskContext {
  readonly metadata: TaskRunMetadata;

  constructor(
    private readonly udsClient: UDSClient,
    input?: GetInputResponse,
  ) {
    this.metadata = {
      taskRunId: input?.task_run_id,
      rootTaskRunId: input?.root_task_run_id || undefined,
      parentTaskRunId: input?.parent_task_run_id,
    };
  }

  async run<TArgs extends unknown[], TResult>(
    task: TaskDefinition<TArgs, TResult>,
    ...args: TArgs
  ): Promise<TResult> {
    const registry = TaskRegistry.getInstance();
    if (!registry.has(task.name)) {
      throw new RenderError(`Task '${task.name}' is not registered`);
    }

    const subtaskId = await this.udsClient.runSubtask(task.name, args);
    return this.awaitSubtask<TResult>(subtaskId);
  }

  /**
   * Poll a submitted subtask until it completes, then unwrap its output.
   */
  private async awaitSubtask<TResult>(subtaskId: string): Promise<TResult> {
    while (true) {
      const result = await this.udsClient.getSubtaskResult(subtaskId);

      if (result.still_running) {
        await new Promise((resolve) => setTimeout(resolve, SUBTASK_POLL_INTERVAL_MS));
        continue;
      }

      if (result.error) {
        throw new RenderError(`Subtask failed: ${result.error.details}`);
      }

      if (result.complete?.output) {
        const json = Buffer.from(result.complete.output, "base64").toString();
        // Task output is wire-encoded as a single-element array.
        return JSON.parse(json)[0] as TResult;
      }

      return undefined as TResult;
    }
  }
}
