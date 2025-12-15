import { Render, ServerError } from '@render/sdk';

/**
 * Example: Using the REST API client to run tasks
 */
async function main() {
  const render = new Render();

  try {
    // Run a task
    console.log('Running task...');

    const result = await render.workflows.runTask('scott-go/square', [4]);

    console.log('Task completed!');
    console.log('Status:', result.status);
    console.log('Results:', result.results);

    // List recent task runs
    console.log('\nListing recent task runs...');
    const taskRuns = await render.workflows.listTaskRuns({ limit: 5 });
    console.log(`Found ${taskRuns.length} task runs:`);
    taskRuns.forEach((run) => {
      console.log(`  - ${run.id}: ${run.status} (${run.taskId})`);
    });

    if (result) {
    // Get specific task run details
      console.log('\nGetting task run details...');
      const details = await render.workflows.getTaskRun(result.id);
      console.log('Task run details:', details);
    }
  } catch (error) {
    if (error instanceof ServerError) {
      console.error('server error', error.name, error.cause)
    }
    console.error('Error:', error);
    process.exit(1);
  }
}

main();
