import { AbortError } from "../errors.js";

/** The longest delay between checks once the backoff has grown. */
const MAX_BACKOFF_INTERVAL_MS = 2000;

type PollOptions<T> = {
  timeoutMs: number;
  /** The first delay between checks. It doubles after each check, up to 2 seconds. A longer one stays fixed. */
  intervalMs: number;
  signal?: AbortSignal;
  /** Builds the error for a timeout, from the last value `load` returned, if any. */
  timeoutError: (last: T | undefined) => Error;
};

type WaitScopeOptions = {
  timeoutMs: number;
  signal?: AbortSignal;
  timeoutError: () => Error;
};

/** Throws `RangeError` for a timeout or interval that `pollUntil` can't use. */
export function validateOptions({
  timeoutMs,
  intervalMs,
}: {
  timeoutMs: number;
  intervalMs: number;
}): void {
  if (!Number.isFinite(timeoutMs) || timeoutMs < 0 || timeoutMs > 2_147_483_647) {
    throw new RangeError("timeoutMs must be between 0 and 2147483647");
  }
  if (!Number.isFinite(intervalMs) || intervalMs <= 0) {
    throw new RangeError("intervalMs must be a positive finite number");
  }
}

function createWaitScope({ timeoutMs, signal, timeoutError }: WaitScopeOptions) {
  const deadline = Date.now() + timeoutMs;
  const controller = new AbortController();
  const onAbort = () => controller.abort(new AbortError());
  const onTimeout = () => controller.abort(timeoutError());
  let rejectOnAbort: (() => void) | undefined;
  const stopped = new Promise<never>((_, reject) => {
    rejectOnAbort = () => reject(controller.signal.reason);
    controller.signal.addEventListener("abort", rejectOnAbort, { once: true });
  });
  signal?.addEventListener("abort", onAbort, { once: true });
  const timer = setTimeout(onTimeout, timeoutMs);

  return {
    deadline,
    signal: controller.signal,
    stopped,
    throwIfStopped() {
      if (Date.now() >= deadline && !controller.signal.aborted) onTimeout();
      controller.signal.throwIfAborted();
    },
    dispose() {
      clearTimeout(timer);
      signal?.removeEventListener("abort", onAbort);
      if (rejectOnAbort) controller.signal.removeEventListener("abort", rejectOnAbort);
    },
  };
}

function sleep(ms: number, signal: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    if (signal.aborted) {
      reject(signal.reason);
      return;
    }
    const onAbort = () => {
      clearTimeout(timer);
      reject(signal.reason);
    };
    const timer = setTimeout(() => {
      signal.removeEventListener("abort", onAbort);
      resolve();
    }, ms);
    signal.addEventListener("abort", onAbort, { once: true });
  });
}

/** Poll until `check` returns a value, or throws when the resource cannot become ready. */
export async function pollUntil<T, R>(
  load: (signal: AbortSignal) => Promise<T>,
  check: (value: T) => R | undefined,
  options: PollOptions<T>,
): Promise<R> {
  if (options.signal?.aborted) throw new AbortError();
  validateOptions(options);
  let last: T | undefined;
  const scope = createWaitScope({ ...options, timeoutError: () => options.timeoutError(last) });
  const maxIntervalMs = Math.max(options.intervalMs, MAX_BACKOFF_INTERVAL_MS);
  const poll = async () => {
    let intervalMs = options.intervalMs;
    for (;;) {
      scope.throwIfStopped();
      const value = await load(scope.signal);
      // The caller asked to stop, so their abort wins even over a success.
      if (options.signal?.aborted) throw new AbortError();
      last = value;
      // Check the status before the deadline, so a resource that is ready by the time a late
      // check returns is returned, not discarded.
      const result = check(value);
      if (result !== undefined) return result;
      scope.throwIfStopped();
      await sleep(Math.min(intervalMs, scope.deadline - Date.now()), scope.signal);
      intervalMs = Math.min(intervalMs * 2, maxIntervalMs);
    }
  };
  try {
    // A custom fetch may ignore cancellation, so also bound the returned promise.
    return await Promise.race([poll(), scope.stopped]);
  } finally {
    scope.dispose();
  }
}
