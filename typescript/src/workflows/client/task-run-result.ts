import type { SSEClient } from "./sse.js";
import type { TaskRunDetails } from "./types.js";

export class TaskRunResult {
  readonly taskRunId: string;
  private readonly sseClient: SSEClient;
  private readonly signal?: AbortSignal;
  private resultPromise: Promise<TaskRunDetails> | null = null;

  constructor(sseClient: SSEClient, taskRunId: string, signal?: AbortSignal) {
    this.sseClient = sseClient;
    this.taskRunId = taskRunId;
    this.signal = signal;
  }

  get(): Promise<TaskRunDetails> {
    if (!this.resultPromise) {
      this.resultPromise = this.sseClient.waitOnTaskRun(this.taskRunId, this.signal);
    }
    return this.resultPromise;
  }
}
