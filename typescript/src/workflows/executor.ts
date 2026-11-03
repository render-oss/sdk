import { RenderError } from "../errors.js";
import { WorkflowTaskContext } from "./context.js";
import { DurableFlowContext } from "./durable/context.js";
import { DeterminismError, WorkflowLimitError } from "./durable/errors.js";
import { decodeArgs } from "./encoding.js";
import { TaskRegistry } from "./registry.js";
import type { FlowMetadata, GetInputResponse, TaskErrorBody } from "./types.js";
import { UDSClient } from "./uds.js";

/**
 * How an execution ended. `stopped` means a workflow attempt was suspended
 * or cancelled: no callback was sent, and the process should wait to be
 * stopped.
 */
export type ExecutionOutcome = "completed" | "stopped";

function errorBody(error: unknown): TaskErrorBody {
  if (!(error instanceof Error)) {
    return { details: String(error) };
  }
  const body: TaskErrorBody = { details: error.message };
  if (error.stack) {
    body.stack_trace = error.stack;
  }
  if (error instanceof DeterminismError) {
    body.reason = "DeterminismError";
    body.determinism = error.details;
  }
  if (error instanceof WorkflowLimitError) {
    body.reason = error.reason;
    body.limit = error.limit;
    body.value = error.value;
  }
  return body;
}

/**
 * The wire input must be a JSON array of positional arguments; no input means
 * no arguments. Anything else would fail the spread with an unclear error.
 */
function argsFromWire(taskName: string, decoded: unknown): unknown[] {
  if (decoded === undefined) {
    return [];
  }
  if (!Array.isArray(decoded)) {
    const got = decoded === null ? "null" : typeof decoded;
    throw new RenderError(
      `Invalid input for '${taskName}': expected an array of the task's arguments, such as [a, b], but got ${got}. To pass an object, wrap it in an array, such as [{ key: "value" }].`,
    );
  }
  return decoded;
}

/**
 * An error that ends the attempt because the workflow system couldn't be
 * reached. The attempt reports a system error if it can, then exits so the
 * platform recovers the run.
 */
export class UnreportedError extends Error {
  constructor(readonly cause: Error) {
    super(`Lost contact with the workflow system: ${cause.message}`);
    this.name = "UnreportedError";
  }
}

/**
 * Task executor that runs tasks via Unix socket communication
 */
export class TaskExecutor {
  private readonly udsClient: UDSClient;

  constructor(socketPath: string) {
    this.udsClient = new UDSClient(socketPath);
  }

  /**
   * Execute a single task
   */
  async executeTask(): Promise<ExecutionOutcome> {
    const registry = TaskRegistry.getInstance();

    try {
      // Get task input
      const input = await this.udsClient.getInput();
      const taskName = input.task_name;
      const inputData = argsFromWire(taskName, decodeArgs(input.input));

      if (input.is_workflow) {
        const flowMetadata = registry.getFlow(taskName);
        if (!flowMetadata) {
          throw new RenderError(
            registry.has(taskName)
              ? `'${taskName}' was started as a workflow but is a plain task`
              : `Workflow '${taskName}' not found in registry`,
          );
        }
        return await this.executeFlow(flowMetadata, input, inputData);
      }

      // Get task from registry
      const taskMetadata = registry.get(taskName);
      if (!taskMetadata) {
        throw new RenderError(
          registry.getFlow(taskName)
            ? `'${taskName}' is a workflow but was started as a plain task`
            : `Task '${taskName}' not found in registry`,
        );
      }

      // The context is always the first argument; the wire input holds the rest.
      const context = new WorkflowTaskContext(this.udsClient, input);
      const result = await taskMetadata.func(context, ...inputData);

      // Send result
      await this.udsClient.sendCallback(result);
      return "completed";
    } catch (error) {
      if (error instanceof UnreportedError) {
        throw error;
      }
      // Send error
      await this.udsClient.sendCallback(undefined, errorBody(error));
      throw error;
    }
  }

  /**
   * Run a workflow attempt until its function settles or the attempt stops:
   * suspended or cancelled (no callback), failed for good (a failure
   * callback), or cut off from the socket (a system error callback, so the
   * run recovers).
   */
  private async executeFlow(
    flowMetadata: FlowMetadata,
    input: GetInputResponse,
    inputData: unknown[],
  ): Promise<ExecutionOutcome> {
    const context = new DurableFlowContext(this.udsClient, input);
    const settled = Promise.resolve()
      .then(() => flowMetadata.func(context, ...inputData))
      .then(
        (value) => ({ kind: "returned" as const, value }),
        (error: unknown) => ({ kind: "threw" as const, error }),
      );
    const outcome = await Promise.race([settled, context.halted]);

    // A halt wins even if user code caught its error and carried on.
    const halt = context.halt;
    if (halt?.kind === "failed") {
      throw halt.error;
    }
    if (halt?.kind === "unreachable") {
      // Render caused this failure, so the callback says so and the run
      // recovers. If the callback can't get through either, the attempt exits
      // without one.
      console.error(`Lost contact with the workflow system: ${halt.error.message}`);
      try {
        await this.udsClient.sendCallback(undefined, {
          details: halt.error.message,
          reason: "system_error",
        });
      } catch (error) {
        console.warn("Could not report the lost contact:", error);
      }
      throw new UnreportedError(halt.error);
    }
    if (halt) {
      return "stopped";
    }

    if (outcome.kind === "threw") {
      throw outcome.error;
    }
    if (outcome.kind === "returned") {
      await this.udsClient.sendCallback(outcome.value);
    }
    return "completed";
  }

  /**
   * Register all tasks with the workflow system
   */
  async registerTasks(): Promise<void> {
    const registry = TaskRegistry.getInstance();
    await this.udsClient.registerTasks(registry.getAllTasks(), registry.getAllFlows());
  }
}
