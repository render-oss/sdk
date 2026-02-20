import type { TaskRunDetails } from "./types.js";

export class TaskRunResult {
  readonly taskRunId: string;
  private readonly waitOnTaskRun: (
    taskRunId: string,
    signal?: AbortSignal,
  ) => Promise<TaskRunDetails>;
  private readonly signal?: AbortSignal;
  private resultPromise: Promise<TaskRunDetails> | null = null;

  constructor(
    waitOnTaskRun: (taskRunId: string, signal?: AbortSignal) => Promise<TaskRunDetails>,
    taskRunId: string,
    signal?: AbortSignal,
  ) {
    this.waitOnTaskRun = waitOnTaskRun;
    this.taskRunId = taskRunId;
    this.signal = signal;
  }

  get(): Promise<TaskRunDetails> {
    if (!this.resultPromise) {
      this.resultPromise = this.waitOnTaskRun(this.taskRunId, this.signal);
    }
    return this.resultPromise;
  }
}
