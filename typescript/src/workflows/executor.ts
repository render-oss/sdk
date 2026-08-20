import { RenderError } from "../errors.js";
import { WorkflowTaskContext } from "./context.js";
import { TaskRegistry } from "./registry.js";
import type { TaskContext } from "./types.js";
import { UDSClient } from "./uds.js";

/**
 * Task executor that runs tasks via Unix socket communication
 */
export class TaskExecutor {
  private readonly udsClient: UDSClient;
  private readonly context: TaskContext;

  constructor(socketPath: string) {
    this.udsClient = new UDSClient(socketPath);
    this.context = new WorkflowTaskContext(this.udsClient);
  }

  /**
   * Execute a single task
   */
  async executeTask(): Promise<void> {
    const registry = TaskRegistry.getInstance();

    try {
      // Get task input
      const input = await this.udsClient.getInput();
      const taskName = input.task_name;
      const inputData = JSON.parse(Buffer.from(input.input, "base64").toString());

      // Get task from registry
      const taskMetadata = registry.get(taskName);
      if (!taskMetadata) {
        throw new RenderError(`Task '${taskName}' not found in registry`);
      }

      // The context is always the first argument; the wire input holds the rest.
      const result = await taskMetadata.func(this.context, ...inputData);

      // Send result
      await this.udsClient.sendCallback(result);
    } catch (error) {
      // Send error
      const errorMessage = error instanceof Error ? error.message : String(error);
      await this.udsClient.sendCallback(undefined, errorMessage);
      throw error;
    }
  }

  /**
   * Register all tasks with the workflow system
   */
  async registerTasks(): Promise<void> {
    const registry = TaskRegistry.getInstance();
    const tasks = registry.getAllTasks();
    await this.udsClient.registerTasks(tasks);
  }
}
