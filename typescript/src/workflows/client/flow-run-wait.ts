import { ClientError, ServerError } from "../../errors.js";
import { pollUntil } from "../../utils/poll-until.js";
import { type FlowRunDetails, FlowRunStatus } from "./types.js";

/** The first delay between status checks. It doubles after each check. */
const INITIAL_INTERVAL_MS = 1000;
/** The longest delay between status checks once the backoff has grown. */
const MAX_INTERVAL_MS = 60_000;
/** How many status checks in a row can fail with a transient error before the wait throws. */
const MAX_CONSECUTIVE_ERRORS = 5;

const FINISHED_STATUSES: ReadonlySet<string> = new Set([
  FlowRunStatus.SUCCEEDED,
  FlowRunStatus.FAILED,
  FlowRunStatus.CANCELED,
]);

/** Returns the details if the flow run has finished, or `undefined` if it may still run. */
export function finishedFlowRun(details: FlowRunDetails): FlowRunDetails | undefined {
  return FINISHED_STATUSES.has(details.status) ? details : undefined;
}

/** Whether a status check that threw `err` is worth trying again. */
export function isTransientError(err: unknown): boolean {
  if (err instanceof ServerError) return true;
  if (err instanceof ClientError) return err.statusCode === 408 || err.statusCode === 429;
  // fetch rejects with a TypeError when the request fails on the network.
  return err instanceof TypeError;
}

/**
 * Wraps `load` so a transient error resolves to `undefined` instead of throwing. After
 * `maxErrors` failures in a row, it throws the last error. A success resets the count.
 */
export function retryTransientErrors<T>(
  load: (signal: AbortSignal) => Promise<T>,
  maxErrors = MAX_CONSECUTIVE_ERRORS,
): (signal: AbortSignal) => Promise<T | undefined> {
  let errors = 0;
  return async (signal) => {
    try {
      const value = await load(signal);
      errors = 0;
      return value;
    } catch (err) {
      errors++;
      if (!isTransientError(err) || errors >= maxErrors) throw err;
    }
  };
}

/**
 * Checks the flow run's status with exponential backoff, from 1 second up to 60 seconds, until
 * it succeeds, fails, or is canceled. Resolves with its details. The wait has no deadline.
 */
export function waitForFlowRun(
  getFlowRun: (flowRunId: string, signal: AbortSignal) => Promise<FlowRunDetails>,
  flowRunId: string,
  signal?: AbortSignal,
): Promise<FlowRunDetails> {
  return pollUntil(
    retryTransientErrors((sig) => getFlowRun(flowRunId, sig)),
    (details) => details && finishedFlowRun(details),
    { intervalMs: INITIAL_INTERVAL_MS, maxIntervalMs: MAX_INTERVAL_MS, signal },
  );
}
