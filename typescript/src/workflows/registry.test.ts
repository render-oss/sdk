import { beforeEach, describe, expect, it } from "vitest";
import { TaskRegistry } from "./registry.js";

describe("TaskRegistry", () => {
  let registry: TaskRegistry;

  beforeEach(() => {
    // Get a fresh registry for each test
    registry = TaskRegistry.getInstance();
    registry.clear();
  });

  describe("register", () => {
    it("should register a task with timeout_seconds", () => {
      const taskFn = () => 42;

      registry.register(taskFn, {
        name: "timeout_task",
        timeoutSeconds: 120,
      });

      const task = registry.get("timeout_task");
      expect(task).toBeDefined();
      expect(task?.options?.timeout_seconds).toBe(120);
    });

    it("should register a task without timeout_seconds", () => {
      const taskFn = () => 42;

      registry.register(taskFn, {
        name: "no_timeout_task",
      });

      const task = registry.get("no_timeout_task");
      expect(task).toBeDefined();
      expect(task?.options).toBeUndefined();
    });

    it("should register a task with both retry and timeout_seconds", () => {
      const taskFn = () => 42;

      registry.register(taskFn, {
        name: "both_options_task",
        timeoutSeconds: 300,
        retry: {
          maxRetries: 3,
          waitDurationMs: 1000,
          backoffScaling: 2.0,
        },
      });

      const task = registry.get("both_options_task");
      expect(task).toBeDefined();
      expect(task?.options?.timeout_seconds).toBe(300);
      expect(task?.options?.retry?.max_retries).toBe(3);
      expect(task?.options?.retry?.wait_duration_ms).toBe(1000);
      expect(task?.options?.retry?.factor).toBe(2.0);
    });

    it("should register a task with only retry options", () => {
      const taskFn = () => 42;

      registry.register(taskFn, {
        name: "retry_only_task",
        retry: {
          maxRetries: 2,
          waitDurationMs: 500,
        },
      });

      const task = registry.get("retry_only_task");
      expect(task).toBeDefined();
      expect(task?.options?.retry?.max_retries).toBe(2);
      expect(task?.options?.timeout_seconds).toBeUndefined();
    });
  });
});
