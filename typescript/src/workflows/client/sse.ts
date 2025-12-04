import { EventSource } from 'eventsource';
import { AbortError } from './errors.js';
import type { TaskRunDetails } from './types.js';

/**
 * Task event types emitted by the SSE stream
 */
export enum TaskEventType {
  COMPLETED = 'task.completed',
  FAILED = 'task.failed',
  RUNNING = 'task.running',
  PENDING = 'task.pending',
}

/**
 * SSE Client for streaming task run events
 */
export class SSEClient {
  constructor(
    private baseUrl: string,
    private token: string
  ) {}

  async waitOnTaskRun(taskRunId: string, signal?: AbortSignal): Promise<TaskRunDetails> {
    return new Promise((resolve, reject) => {
      let eventSource: EventSource | null = null;

      const abortHandler = () => {
        cleanup();
        reject(new AbortError());
      };

      const cleanup = () => {
        if (eventSource) {
          eventSource.removeEventListener(TaskEventType.COMPLETED, eventHandler);
          eventSource.removeEventListener(TaskEventType.FAILED, eventHandler);
          eventSource.removeEventListener('error', errorHandler);
          eventSource.close();
          eventSource = null;
        }
        signal?.removeEventListener('abort', abortHandler);
      };

      const eventHandler = (event: MessageEvent) => {
        try {
          const details = JSON.parse(event.data) as TaskRunDetails;
          cleanup();
          resolve(details);
        } catch (e) {
          cleanup();
          reject(new Error(`Failed to parse task run details: ${e}`));
        }
      };

      const errorHandler = (error: any) => {
        cleanup();
        reject(new Error(`SSE connection error: ${error.message || 'Unknown error'}`));
      };

      // Check if already aborted
      if (signal?.aborted) {
        reject(new AbortError());
        return;
      }

      // Listen for abort signal
      signal?.addEventListener('abort', abortHandler);

      try {
        const url = new URL('/v1/task-runs/events', this.baseUrl);
        url.searchParams.append('taskRunIds', taskRunId);

        eventSource = new EventSource(url.toString(), {
          fetch: (input, init) =>
            fetch(input, {
              ...init,
              headers: {
                ...init?.headers,
                Authorization: `Bearer ${this.token}`,
              },
            }),
        });

        eventSource.addEventListener(TaskEventType.COMPLETED, eventHandler);
        eventSource.addEventListener(TaskEventType.FAILED, eventHandler);
        eventSource.addEventListener('error', errorHandler);
      } catch (e) {
        cleanup();
        reject(e);
      }
    });
  }
}
