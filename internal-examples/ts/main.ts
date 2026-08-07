/** Example usage of the Render Tasks TypeScript SDK. */

import { task } from "@renderinc/sdk/workflows";

/**
 * Deadlock test example.
 *
 * If we don't properly mark parent tasks waiting on subtasks, we can deadlock
 * the workflow. This will spawn a chain of n tasks that will each wait for the
 * next sub task to complete. If n > the max concurrency limit we will deadlock
 * the workflow if our pause logic is not working.
 */
const deadlockTest = task({ name: "deadlockTest" }, async (n: number): Promise<number> => {
  if (n > 0) {
    // Call through the registered wrapper so each level runs as its own subtask.
    await deadlockTest(n - 1);
  }

  console.info(`Deadlock test ${n} complete`);

  return n;
});

/**
 * Prints a simple string.
 */
task({ name: "printHelloWorld" }, (): void => {
  console.log("Hello, world!");
});

/**
 * Emits a series of log messages at different log levels.
 */
task({ name: "emitLogs" }, (): void => {
  console.debug("Logging to DEBUG");
  console.info("Logging to INFO");
  console.warn("Logging to WARNING");
  console.error("Logging to ERROR");
});

/**
 * Calculate the square of a number.
 */
const calculateSquare = task({ name: "calculateSquare" }, (n: number): number => {
  return n * n;
});

/**
 * Add the squares of two numbers.
 */
task({ name: "addSquares" }, async (a: number, b: number): Promise<number> => {
  console.info(`Computing addSquares: ${a}, ${b}`);

  // Execute subtasks
  const result1 = await calculateSquare(a);
  console.info(`Square result 1: ${result1}`);
  const result2 = await calculateSquare(b);
  console.info(`Square result 2: ${result2}`);

  return result1 + result2;
});
