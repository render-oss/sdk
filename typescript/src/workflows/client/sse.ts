/**
 * Task event types emitted by the SSE stream
 */
export enum TaskEventType {
  COMPLETED = "task.completed",
  FAILED = "task.failed",
  RUNNING = "task.running",
  PENDING = "task.pending",
}
