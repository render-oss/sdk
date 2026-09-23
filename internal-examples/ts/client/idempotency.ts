/**
 * Render TypeScript Client — idempotency key check
 *
 * Submits the same task three times: twice under one idempotency key and once
 * under a different one. Two submissions sharing a key must resolve to a single
 * task run; a different key must start a new one.
 *
 * Setup:
 *   export RENDER_API_KEY="your_token_here"
 *   export RENDER_TASK_SLUG="my-workflow-slug/task-name"
 *   export RENDER_TASK_INPUT='[4]'   # optional, defaults to [4]
 *   npm run idempotency
 *
 * To run against local dev also set:
 *   export RENDER_LOCAL_DEV_URL="https://api.localhost.render.com:8443"
 */

import { randomUUID } from "node:crypto";
import { Render } from "@renderinc/sdk";
import type { TaskRunDetails } from "@renderinc/sdk/workflows";

const TERMINAL = new Set(["completed", "succeeded", "failed", "canceled"]);

const TRUTHY = new Set(["1", "t", "T", "true", "TRUE", "True"]);

async function waitForTerminal(
  render: Render,
  taskRunId: string,
  timeoutMs = 180_000,
): Promise<TaskRunDetails> {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    const details = await render.workflows.getTaskRun(taskRunId);
    if (TERMINAL.has(details.status)) {
      return details;
    }
    if (Date.now() > deadline) {
      throw new Error(`${taskRunId} still ${details.status}`);
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
}

async function main(): Promise<number> {
  const taskSlug = process.env.RENDER_TASK_SLUG;
  if (!taskSlug) {
    console.error("RENDER_TASK_SLUG is required, e.g. my-workflow/square");
    return 2;
  }
  const inputData = JSON.parse(process.env.RENDER_TASK_INPUT ?? "[4]");

  const render = new Render();

  // Fresh keys every run. A key stays claimed for 24 hours, so reusing one
  // across runs would resolve to the previous run rather than testing anything.
  const sharedKey = `sdk-idempotency-check-${randomUUID()}`;
  const otherKey = `sdk-idempotency-check-${randomUUID()}`;
  console.log(`task:       ${taskSlug}`);
  console.log(`shared key: ${sharedKey}`);
  console.log(`other key:  ${otherKey}\n`);

  const first = await render.workflows.startTask(taskSlug, inputData, {
    idempotencyKey: sharedKey,
  });
  console.log(`1. submitted with shared key -> ${first.taskRunId}`);

  const repeat = await render.workflows.startTask(taskSlug, inputData, {
    idempotencyKey: sharedKey,
  });
  console.log(`2. resubmitted same key      -> ${repeat.taskRunId}`);

  const different = await render.workflows.startTask(taskSlug, inputData, {
    idempotencyKey: otherKey,
  });
  console.log(`3. submitted with other key  -> ${different.taskRunId}`);

  const failures: string[] = [];
  if (repeat.taskRunId !== first.taskRunId) {
    failures.push(
      `reusing a key started a second run (${first.taskRunId} then ${repeat.taskRunId})`,
    );
  }
  if (different.taskRunId === first.taskRunId) {
    failures.push(`a different key resolved to the first run (${first.taskRunId})`);
  }

  console.log("\nwaiting for both runs to finish...");
  const firstDetails = await waitForTerminal(render, first.taskRunId);
  const differentDetails = await waitForTerminal(render, different.taskRunId);
  console.log(`   ${first.taskRunId}: ${firstDetails.status}`, firstDetails.results);
  console.log(
    `   ${different.taskRunId}: ${differentDetails.status}`,
    differentDetails.results,
  );

  // A claim outlives the run it created, so replaying the key after the run
  // finishes returns that finished run rather than starting a fresh one.
  const replay = await render.workflows.startTask(taskSlug, inputData, {
    idempotencyKey: sharedKey,
  });
  console.log(`\n4. replayed shared key after completion -> ${replay.taskRunId}`);
  if (replay.taskRunId !== first.taskRunId) {
    failures.push(
      `replaying a key after completion started a new run (${replay.taskRunId})`,
    );
  }

  console.log();
  if (failures.length > 0) {
    for (const failure of failures) {
      console.error(`FAIL: ${failure}`);
    }
    return 1;
  }
  console.log("PASS: one key produced one run, a second key produced another");
  return 0;
}

main()
  .then((code) => process.exit(code))
  .catch((err) => {
    // Reaching the wrong server, or none at all, is the common way to run this:
    // report it as that rather than as a failed assertion.
    console.error(`\nERROR: ${err instanceof Error ? err.message : err}`);
    console.error(
      "Check the base url. For a local dev server set RENDER_LOCAL_DEV_URL."
    );
    process.exit(3);
  });
