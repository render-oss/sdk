import { task, startTaskServer } from '@render/sdk/workflows';

/**
 * Simple task that squares a number
 */
const square = task(
    { name: "square" },
  function square(a: number): number {
    console.log(`Calculating square of ${a}`);
    return a * a;
  }
)

/**
 * Async task that adds two squared numbers with custom options
 */
task(
  {
    name: "addSquares",
    retry: {
      maxRetries: 3,
      waitDurationMs: 1000,
      factor: 1.5,
    },
  },
  async function addSquares(a: number, b: number): Promise<number> {
    console.log(`Adding squares of ${a} and ${b}`);

    // Execute subtasks (these will be executed by the workflow system)
    const result1 = await square(a);
    console.log("result 1", result1);
    const result2 = await square(b);
    console.log("result 2", result2)

    const sum = result1 + result2;
    console.log(`Result: ${result1} + ${result2} = ${sum}`);
    return sum;
  }
)

/**
 * Task with error handling
 */
const divide = task(
  { name: "divide" },
  async function divide(a: number, b: number): Promise<number> {
    if (b === 0) {
      throw new Error('Cannot divide by zero');
    }
    return a / b;
  }
);

/**
 * Complex task that chains multiple operations
 */
task(
  { name: "complexCalculation" },
  async function complexCalculation(x: number, y: number, z: number): Promise<number> {
    console.log(`Complex calculation: x=${x}, y=${y}, z=${z}`);

    // Square x and y
    const xSquared = await square(x);
    const ySquared = await square(y);

    // Add the squares
    const sum = xSquared + ySquared;

    // Divide by z
    const result = await divide(sum, z);

    console.log(`Complex result: (${x}^2 + ${y}^2) / ${z} = ${result}`);
    return result;
  }
);

task(
  {
    name: "errorFunction",
    retry: {
      maxRetries: 10,
      waitDurationMs: 1000
    }
  },
  function () {
    throw new Error("this failed on purpose")
  }
)

/**
 * Start the task server
 */
console.log('Starting task server...');

(async () => {
  try {
    await startTaskServer();
    console.log('Task server started successfully');
  } catch (error) {
    console.error('Failed to start task server:', error);
    process.exit(1);
  }
})();
