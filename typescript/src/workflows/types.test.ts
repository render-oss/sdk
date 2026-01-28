import type { TaskContext, TaskFunction, TaskResult } from "./types.js";

describe("TaskFunction type", () => {
  it("accepts typed args and returns typed result", () => {
    expectTypeOf<TaskFunction<[string, number], boolean>>().toExtend<
      (a: string, b: number) => boolean | Promise<boolean>
    >();
  });

  it("defaults to any[] args and any result", () => {
    expectTypeOf<TaskFunction>().toExtend<(...args: any[]) => any>();
  });

  it("allows async return type", () => {
    const asyncFn: TaskFunction<[string], number> = async (s) => s.length;
    expectTypeOf(asyncFn).returns.toExtend<number | Promise<number>>();
  });

  it("allows sync return type", () => {
    const syncFn: TaskFunction<[string], number> = (s) => s.length;
    expectTypeOf(syncFn).returns.toExtend<number | Promise<number>>();
  });
});

describe("TaskResult type", () => {
  it("get() returns Promise<T>", () => {
    expectTypeOf<TaskResult<string>>().toHaveProperty("get");
    expectTypeOf<TaskResult<string>["get"]>().returns.toEqualTypeOf<Promise<string>>();
  });

  it("preserves generic parameter", () => {
    type NumberResult = TaskResult<number>;
    type StringResult = TaskResult<string>;
    expectTypeOf<NumberResult["get"]>().returns.toEqualTypeOf<Promise<number>>();
    expectTypeOf<StringResult["get"]>().returns.toEqualTypeOf<Promise<string>>();
  });
});

describe("TaskContext type", () => {
  it("has executeTask method", () => {
    expectTypeOf<TaskContext>().toHaveProperty("executeTask");
  });

  it("executeTask is callable", () => {
    type ExecuteTask = TaskContext["executeTask"];
    expectTypeOf<ExecuteTask>().toBeCallableWith(
      {} as TaskFunction<[string], number>,
      "taskName",
      "arg",
    );
  });
});
