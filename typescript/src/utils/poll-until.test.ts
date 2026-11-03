import { AbortError } from "../errors.js";
import { pollUntil, validateOptions } from "./poll-until.js";

// A load that reports "waiting" until its `readyOnCall`th call, then "ready".
function newLoad(readyOnCall: number) {
  const calledAt: number[] = [];
  const load = vi.fn(async (_signal: AbortSignal) => {
    calledAt.push(Date.now());
    return calledAt.length >= readyOnCall ? "ready" : "waiting";
  });
  return { load, calledAt };
}

const ready = (value: string) => (value === "ready" ? value : undefined);

function delaysBetween(times: number[]): number[] {
  return times.slice(1).map((t, i) => t - times[i]);
}

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

describe("pollUntil", () => {
  it.each([
    {
      name: "doubles up to 2 seconds by default",
      intervalMs: 100,
      maxIntervalMs: undefined,
      delays: [100, 200, 400, 800, 1600, 2000, 2000],
    },
    {
      name: "doubles up to maxIntervalMs",
      intervalMs: 1000,
      maxIntervalMs: 10_000,
      delays: [1000, 2000, 4000, 8000, 10_000, 10_000],
    },
    {
      name: "keeps an interval longer than maxIntervalMs fixed",
      intervalMs: 3000,
      maxIntervalMs: undefined,
      delays: [3000, 3000],
    },
  ])("backs off and $name", async ({ intervalMs, maxIntervalMs, delays }) => {
    const { load, calledAt } = newLoad(delays.length + 1);

    const result = pollUntil(load, ready, { intervalMs, maxIntervalMs });
    await vi.advanceTimersByTimeAsync(60_000);

    await expect(result).resolves.toBe("ready");
    expect(delaysBetween(calledAt)).toEqual(delays);
  });

  it("polls past any deadline when timeoutMs is omitted", async () => {
    // About half an hour of 2-second checks.
    const { load } = newLoad(1000);

    const result = pollUntil(load, ready, { intervalMs: 1000 });
    await vi.advanceTimersByTimeAsync(1000 * 2000);

    await expect(result).resolves.toBe("ready");
  });

  it.each([
    { name: "sets no timer when timeoutMs is omitted", timeout: {}, timers: 0 },
    {
      name: "sets a timer for timeoutMs",
      timeout: { timeoutMs: 5000, timeoutError: () => new Error("timed out") },
      timers: 1,
    },
  ])("$name", async ({ timeout, timers }) => {
    const controller = new AbortController();
    const load = () => new Promise<string>(() => {});

    const result = pollUntil(load, ready, {
      intervalMs: 1000,
      signal: controller.signal,
      ...timeout,
    }).catch((err: unknown) => err);

    expect(vi.getTimerCount()).toBe(timers);
    controller.abort();
    expect(await result).toBeInstanceOf(AbortError);
  });
});

describe("validateOptions", () => {
  it.each([
    { name: "no timeoutMs", options: { intervalMs: 1000 } },
    { name: "a timeoutMs", options: { timeoutMs: 1000, intervalMs: 1000 } },
    { name: "a maxIntervalMs", options: { intervalMs: 1000, maxIntervalMs: 10_000 } },
  ])("accepts $name", ({ options }) => {
    expect(() => validateOptions(options)).not.toThrow();
  });

  it.each([
    { name: "a negative timeoutMs", options: { timeoutMs: -1, intervalMs: 1000 } },
    { name: "a zero intervalMs", options: { intervalMs: 0 } },
    { name: "a zero maxIntervalMs", options: { intervalMs: 1000, maxIntervalMs: 0 } },
    {
      name: "an infinite maxIntervalMs",
      options: { intervalMs: 1000, maxIntervalMs: Number.POSITIVE_INFINITY },
    },
  ])("rejects $name", ({ options }) => {
    expect(() => validateOptions(options)).toThrow(RangeError);
  });
});
