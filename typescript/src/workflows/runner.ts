import { RenderError } from './client/errors.js';
import { TaskExecutor } from './executor.js';

/**
 * Start the task server and listen for task execution requests
 */
export async function startTaskServer(): Promise<void> {
  const mode = process.env.RENDER_SDK_MODE || 'run';
  const socketPath = process.env.RENDER_SDK_SOCKET_PATH;

  if (!socketPath) {
    throw new RenderError('RENDER_SDK_SOCKET_PATH environment variable is required');
  }

  const executor = new TaskExecutor(socketPath);

  if (mode === 'register') {
    // Register tasks mode
    await executor.registerTasks();
  } else if (mode === 'run') {
    // Run task mode
    await executor.executeTask();
  } else {
    throw new RenderError(`Unknown SDK mode: ${mode}`);
  }
}

/**
 * Run a specific task (for testing or direct execution)
 */
export async function run(socketPath: string): Promise<void> {
  const executor = new TaskExecutor(socketPath);
  await executor.executeTask();
}
