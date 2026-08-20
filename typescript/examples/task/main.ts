import { type TaskContext, task } from "@renderinc/sdk/workflows";

/**
 * Simple task that squares a number.
 *
 * Every task takes a TaskContext as its first parameter, followed by its
 * inputs. This one has no subtasks, so it never touches the context.
 */
const square = task({ name: "square" }, function square(_ctx: TaskContext, a: number): number {
  console.log(`Calculating square of ${a}`);
  return a * a;
});

/**
 * Async task that adds two squared numbers with custom options.
 *
 * Subtasks are reached through the context: ctx.run runs the task on its
 * own compute and resolves with its result.
 */
task(
  {
    name: "addSquares",
    retry: {
      maxRetries: 3,
      waitDurationMs: 1000,
      backoffScaling: 1.5,
    },
  },
  async function addSquares(ctx: TaskContext, a: number, b: number): Promise<number> {
    console.log(`Adding squares of ${a} and ${b}`);

    const result1 = await ctx.run(square, a);
    console.log("result 1", result1);
    const result2 = await ctx.run(square, b);
    console.log("result 2", result2);

    const sum = result1 + result2;
    console.log(`Result: ${result1} + ${result2} = ${sum}`);
    return sum;
  },
);

/**
 * Task with error handling
 */
const divide = task(
  { name: "divide" },
  async function divide(_ctx: TaskContext, a: number, b: number): Promise<number> {
    if (b === 0) {
      throw new Error("Cannot divide by zero");
    }
    return a / b;
  },
);

/**
 * Complex task that chains multiple operations.
 *
 * Independent subtasks can be run concurrently.
 */
task(
  { name: "complexCalculation" },
  async function complexCalculation(
    ctx: TaskContext,
    x: number,
    y: number,
    z: number,
  ): Promise<number> {
    console.log(`Complex calculation: x=${x}, y=${y}, z=${z}`);

    // Square x and y
    const [xSquared, ySquared] = await Promise.all([ctx.run(square, x), ctx.run(square, y)]);

    // Add the squares
    const sum = xSquared + ySquared;

    // Divide by z
    const result = await ctx.run(divide, sum, z);

    console.log(`Complex result: (${x}^2 + ${y}^2) / ${z} = ${result}`);
    return result;
  },
);

task(
  {
    name: "errorFunction",
    retry: {
      maxRetries: 10,
      waitDurationMs: 1000,
    },
  },
  (_ctx: TaskContext) => {
    throw new Error("this failed on purpose");
  },
);

// The task server starts automatically when running in a workflow environment
// (when RENDER_SDK_SOCKET_PATH is set). No need to call startTaskServer() explicitly.
//
// To disable auto-start, set RENDER_SDK_AUTO_START=false in your environment.
