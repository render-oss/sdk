import { Render, ServerError } from "@renderinc/sdk";

/**
 * Example: Using the REST API client to run tasks
 *
 * runTask() starts a task and waits for its result in one call.
 * startTask() starts a task and returns a TaskRunResult, letting you
 * decide when (or whether) to await the result via .get().
 */
async function main() {
  const render = new Render();

  try {
    // Run a task and wait for its result in one call.
    const result = await render.workflows.runTask("my-workflow/square", [4]);
    console.log("Task completed:", result.status, result.results);

    // Start a task and grab its ID for later use (e.g. polling, logging).
    // Results aren't streamed until you call .get() to await the result.
    const run = await render.workflows.startTask("my-workflow/square", [7]);
    console.log("Started task run:", run.taskRunId);
    const result2 = await run.get();
    console.log("Task completed:", result2.status, result2.results);

    // Fire-and-forget: start a task without waiting for the result.
    // .catch() prevents an unhandled rejection if the POST fails.
    render.workflows.startTask("my-workflow/square", [10]).catch((err) => {
      console.error("fire-and-forget task failed to start:", err);
    });

    // Cancel a task run by ID
    const run2 = await render.workflows.startTask("my-workflow/square", [99]);
    await render.workflows.cancelTaskRun(run2.taskRunId);
    console.log("Cancelled task run:", run2.taskRunId);

    // List recent task runs
    const taskRuns = await render.workflows.listTaskRuns({ limit: 5 });
    console.log(`\nFound ${taskRuns.length} task runs:`);
    for (const taskRun of taskRuns) {
      console.log(`  - ${taskRun.id}: ${taskRun.status} (${taskRun.taskId})`);
    }

    // Get task run details by ID
    const details = await render.workflows.getTaskRun(result.id);
    console.log("\nTask run details:", details);
  } catch (error) {
    if (error instanceof ServerError) {
      console.error("server error", error.name, error.message);
    }
    console.error("Error:", error);
    process.exit(1);
  }
}

main();
