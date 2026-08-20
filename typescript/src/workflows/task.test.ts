import { TaskRegistry } from "./registry.js";
import { task } from "./task.js";
import type { TaskContext, TaskDefinition } from "./types.js";

/**
 * A context that resolves runs in process, so tasks can be exercised
 * without a workflow environment.
 */
const localContext: TaskContext = {
  run: <TArgs extends unknown[], TResult>(
    definition: TaskDefinition<TArgs, TResult>,
    ...args: TArgs
  ) => Promise.resolve(definition.func(localContext, ...args)),
};

describe("task", () => {
  beforeEach(() => {
    TaskRegistry.getInstance().clear();
  });

  it("registers the function under the given name", () => {
    const square = task({ name: "square" }, (_ctx, a: number) => a * a);

    const metadata = TaskRegistry.getInstance().get("square");
    expect(metadata?.name).toBe("square");
    expect(metadata?.func).toBe(square.func);
  });

  it("exposes the registered name on the definition", () => {
    const square = task({ name: "square" }, (_ctx, a: number) => a * a);

    expect(square.name).toBe("square");
  });

  it("registers the options alongside the function", () => {
    task({ name: "withOptions", timeoutSeconds: 90, plan: "pro" }, (_ctx: TaskContext) => 1);

    const metadata = TaskRegistry.getInstance().get("withOptions");
    expect(metadata?.options?.timeout_seconds).toBe(90);
    expect(metadata?.options?.plan).toBe("pro");
  });

  it("exposes the function for direct in-process invocation", async () => {
    const square = task({ name: "square" }, (_ctx, a: number) => a * a);

    // This is the undecorated function, so a sync task stays sync.
    expect(await square.func(localContext, 4)).toBe(16);
  });

  it("is not callable, so an old-style square(5) throws rather than binding 5 to ctx", () => {
    const square = task({ name: "square" }, (_ctx, a: number) => a * a);

    expect(typeof square).toBe("object");
    expect(() => (square as unknown as () => void)()).toThrow(TypeError);
  });

  it("supports a variadic task", async () => {
    const sum = task({ name: "sum" }, (_ctx, ...values: number[]) =>
      values.reduce((a, b) => a + b, 0),
    );

    await expect(localContext.run(sum, 1, 2, 3)).resolves.toBe(6);
    await expect(localContext.run(sum)).resolves.toBe(0);
  });

  it("lets a task reach another task through its context", async () => {
    const square = task({ name: "square" }, (_ctx, a: number) => a * a);
    const sumSquares = task({ name: "sumSquares" }, async (ctx, a: number, b: number) => {
      const [a2, b2] = await Promise.all([ctx.run(square, a), ctx.run(square, b)]);
      return a2 + b2;
    });

    await expect(localContext.run(sumSquares, 3, 4)).resolves.toBe(25);
  });
});
