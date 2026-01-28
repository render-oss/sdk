import {
  AbortError,
  ClientError,
  RenderError,
  ServerError,
  TaskRunError,
  TimeoutError,
} from "./errors.js";

describe("errors", () => {
  describe("RenderError", () => {
    it("has correct name and message", () => {
      const err = new RenderError("test message");
      expect(err.name).toBe("RenderError");
      expect(err.message).toBe("test message");
      expect(err instanceof Error).toBe(true);
      expect(err instanceof RenderError).toBe(true);
    });
  });

  describe("TaskRunError", () => {
    it("has correct name and properties", () => {
      const err = new TaskRunError("task failed", "run-123", "internal error");
      expect(err.name).toBe("TaskRunError");
      expect(err.message).toBe("task failed");
      expect(err.taskRunId).toBe("run-123");
      expect(err.taskError).toBe("internal error");
      expect(err instanceof RenderError).toBe(true);
    });

    it("works with optional properties", () => {
      const err = new TaskRunError("task failed");
      expect(err.taskRunId).toBeUndefined();
      expect(err.taskError).toBeUndefined();
    });
  });

  describe("ClientError", () => {
    it("has correct name and properties", () => {
      const err = new ClientError("not found", 404, { detail: "missing" });
      expect(err.name).toBe("ClientError");
      expect(err.statusCode).toBe(404);
      expect(err.response).toEqual({ detail: "missing" });
      expect(err instanceof RenderError).toBe(true);
    });
  });

  describe("ServerError", () => {
    it("has correct name and properties", () => {
      const err = new ServerError("server error", 500, { detail: "crash" });
      expect(err.name).toBe("ServerError");
      expect(err.statusCode).toBe(500);
      expect(err.response).toEqual({ detail: "crash" });
      expect(err instanceof RenderError).toBe(true);
    });
  });

  describe("TimeoutError", () => {
    it("has correct name and inherits from RenderError", () => {
      const err = new TimeoutError("request timed out");
      expect(err.name).toBe("TimeoutError");
      expect(err.message).toBe("request timed out");
      expect(err instanceof RenderError).toBe(true);
    });
  });

  describe("AbortError", () => {
    it("has correct name and fixed message", () => {
      const err = new AbortError();
      expect(err.name).toBe("AbortError");
      expect(err.message).toBe("The operation was aborted.");
      expect(err instanceof Error).toBe(true);
    });
  });
});
