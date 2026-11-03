import { AbortError } from "../errors.js";

/** The default longest delay between checks once the backoff has grown. */
const DEFAULT_MAX_INTERVAL_MS = 2000;

type PollOptions<T> = {
  /** The first delay between checks. It doubles after each check, up to `maxIntervalMs`. A longer one stays fixed. */
  intervalMs: number;
  /** The longest delay between checks once the backoff has grown. Defaults to 2 seconds. */
  maxIntervalMs?: number;
  signal?: AbortSignal;
} & (
  | {
      timeoutMs: number;
      /** Builds the error for a timeout, from the last value `load` returned, if any. */
      timeoutError: (last: T | undefined) => Error;
    }
  | {
      /** Omitted, the poll has no deadline. */
      timeoutMs?: undefined;
      timeoutError?: undefined;
    }
);

type WaitScopeOptions = {
  timeoutMs?: number;
  signal?: AbortSignal;
  timeoutError?: () => Error;
};

/** Throws `RangeError` for a timeout or interval that `pollUntil` can't use. */
export function validateOptions({
  timeoutMs,
  intervalMs,
  maxIntervalMs,
}: {
  timeoutMs?: number;
  intervalMs: number;
  maxIntervalMs?: number;
}): void {
  if (
    timeoutMs !== undefined &&
    (!Number.isFinite(timeoutMs) || timeoutMs < 0 || timeoutMs > 2_147_483_647)
  ) {
    throw new RangeError("timeoutMs must be between 0 and 2147483647");
  }
  if (!Number.isFinite(intervalMs) || intervalMs <= 0) {
    throw new RangeError("intervalMs must be a positive finite number");
  }
  if (maxIntervalMs !== undefined && (!Number.isFinite(maxIntervalMs) || maxIntervalMs <= 0)) {
    throw new RangeError("maxIntervalMs must be a positive finite number");
  }
}

/** Without a `timeoutMs`, the scope has no deadline and sets no timer. */
function createWaitScope({ timeoutMs, signal, timeoutError }: WaitScopeOptions) {
  const deadline = timeoutMs === undefined ? Number.POSITIVE_INFINITY : Date.now() + timeoutMs;
  const controller = new AbortController();
  const onAbort = () => controller.abort(new AbortError());
  const onTimeout = () => controller.abort(timeoutError?.());
  let rejectOnAbort: (() => void) | undefined;
  const stopped = new Promise<never>((_, reject) => {
    rejectOnAbort = () => reject(controller.signal.reason);
    controller.signal.addEventListener("abort", rejectOnAbort, { once: true });
  });
  signal?.addEventListener("abort", onAbort, { once: true });
  const timer = timeoutMs === undefined ? undefined : setTimeout(onTimeout, timeoutMs);

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
  const { timeoutError } = options;
  const scope = createWaitScope({
    timeoutMs: options.timeoutMs,
    signal: options.signal,
    timeoutError: timeoutError && (() => timeoutError(last)),
  });
  const maxIntervalMs = Math.max(
    options.intervalMs,
    options.maxIntervalMs ?? DEFAULT_MAX_INTERVAL_MS,
  );
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
