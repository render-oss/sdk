import { RenderError } from "../errors.js";
import { markSdkStarted } from "../startup.js";
import { TaskExecutor } from "./executor.js";
import { markServerStarted } from "./task.js";

/**
 * Start the task server and listen for task execution requests
 */
export async function startTaskServer(): Promise<void> {
  const mode = process.env.RENDER_SDK_MODE || "run";
  if (mode === "run") markSdkStarted();
  const socketPath = process.env.RENDER_SDK_SOCKET_PATH;

  if (!socketPath) {
    throw new RenderError("RENDER_SDK_SOCKET_PATH environment variable is required");
  }

  const executor = new TaskExecutor(socketPath);

  // Mark server as started to warn about late task registrations
  markServerStarted();

  if (mode === "register") {
    // Register tasks mode
    await executor.registerTasks();
  } else if (mode === "run") {
    // Run task mode
    if ((await executor.executeTask()) === "stopped") {
      await waitToBeStopped();
    }
  } else {
    throw new RenderError(`Unknown SDK mode: ${mode}`);
  }
}

/**
 * Run a specific task (for testing or direct execution)
 */
export async function run(socketPath: string): Promise<void> {
  markSdkStarted();
  const executor = new TaskExecutor(socketPath);
  if ((await executor.executeTask()) === "stopped") {
    await waitToBeStopped();
  }
}

/**
 * Keep the process alive after a workflow attempt suspends or is cancelled.
 * The workflow system stops the process; exiting first would look like a
 * crash.
 */
function waitToBeStopped(): Promise<never> {
  return new Promise(() => {
    setInterval(() => {}, 1 << 30);
  });
}
