/**
 * Task event types emitted by the SSE stream
 *
 * NOTE: right now, the API emits all terminal events as "task.completed" events
 * regardless of status. The true event status is contained elsewhere in the
 * event data. These are here for forward compatibility.
 */
export enum TaskEventType {
  COMPLETED = "task.completed", // deprecated, use SUCCEEDED instead
  SUCCEEDED = "task.succeeded",
  FAILED = "task.failed",
  CANCELED = "task.canceled",
  RUNNING = "task.running",
  PENDING = "task.pending",
}
