/**
 * Task event types emitted by the SSE stream
 */
export enum TaskEventType {
  COMPLETED = "task.completed",
  FAILED = "task.failed",
  CANCELED = "task.canceled",
  RUNNING = "task.running",
  PENDING = "task.pending",
}
