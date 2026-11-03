import { AbortError, ClientError, ServerError } from "../../errors.js";
import { waitForFlowRun } from "./flow-run-wait.js";
import { type FlowRunDetails, FlowRunStatus } from "./types.js";

function details(status: `${FlowRunStatus}`): FlowRunDetails {
  return { id: "frn-1", flowId: "flw-1", status, input: [], results: [], attempts: [] };
}

// A fake getFlowRun that returns or throws each response in turn and repeats the last one.
function fakeGetFlowRun(responses: (FlowRunDetails | Error)[]) {
  const calledAt: number[] = [];
  const getFlowRun = vi.fn(async (_flowRunId: string, _signal: AbortSignal) => {
    calledAt.push(Date.now());
    const next = responses.length > 1 ? responses.shift() : responses[0];
    if (next instanceof Error) throw next;
    return next as FlowRunDetails;
  });
  return { getFlowRun, calledAt };
}

// Starts a wait against a fake getFlowRun, with a rejection handler attached so a test can
// advance the timers before it asserts.
function startWait(responses: (FlowRunDetails | Error)[], signal?: AbortSignal) {
  const fake = fakeGetFlowRun(responses);
  const promise = waitForFlowRun(fake.getFlowRun, "frn-1", signal);
  const settled = promise.then(
    (value) => ({ value, error: undefined }),
    (error: unknown) => ({ value: undefined, error }),
  );
  return { ...fake, settled };
}

function delaysBetween(times: number[]): number[] {
  return times.slice(1).map((t, i) => t - times[i]);
}

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

describe("waitForFlowRun", () => {
  it("backs off from 1 second, doubling up to 60 seconds", async () => {
    const running = Array.from({ length: 8 }, () => details(FlowRunStatus.RUNNING));
    const { calledAt, settled } = startWait([...running, details(FlowRunStatus.SUCCEEDED)]);

    await vi.advanceTimersByTimeAsync(300_000);

    expect((await settled).value?.status).toBe(FlowRunStatus.SUCCEEDED);
    expect(delaysBetween(calledAt)).toEqual([
      1000, 2000, 4000, 8000, 16_000, 32_000, 60_000, 60_000,
    ]);
  });

  it.each([
    {
      name: "keeps polling through pending, running, and paused",
      responses: [
        details(FlowRunStatus.PENDING),
        details(FlowRunStatus.RUNNING),
        details(FlowRunStatus.PAUSED),
        details(FlowRunStatus.PAUSED),
        details(FlowRunStatus.SUCCEEDED),
      ],
      status: FlowRunStatus.SUCCEEDED,
      calls: 5,
    },
    {
      name: "resolves with a failed run",
      responses: [details(FlowRunStatus.RUNNING), details(FlowRunStatus.FAILED)],
      status: FlowRunStatus.FAILED,
      calls: 2,
    },
    {
      name: "resolves with a canceled run",
      responses: [details(FlowRunStatus.CANCELED)],
      status: FlowRunStatus.CANCELED,
      calls: 1,
    },
    {
      name: "keeps polling through transient errors",
      responses: [
        new ServerError("boom", 502),
        new ClientError("busy", 429),
        new TypeError("fetch failed"),
        details(FlowRunStatus.SUCCEEDED),
      ],
      status: FlowRunStatus.SUCCEEDED,
      calls: 4,
    },
  ])("$name", async ({ responses, status, calls }) => {
    const { getFlowRun, settled } = startWait(responses);

    await vi.advanceTimersByTimeAsync(60_000);

    expect((await settled).value?.status).toBe(status);
    expect(getFlowRun).toHaveBeenCalledTimes(calls);
  });

  it.each([
    {
      name: "the 5th transient error in a row",
      responses: [new ServerError("boom", 503)],
      error: ServerError,
      calls: 5,
    },
    {
      name: "a non-transient error",
      responses: [details(FlowRunStatus.RUNNING), new ClientError("gone", 404)],
      error: ClientError,
      calls: 2,
    },
  ])("rejects with $name", async ({ responses, error, calls }) => {
    const { getFlowRun, settled } = startWait(responses);

    await vi.advanceTimersByTimeAsync(60_000);

    expect((await settled).error).toBeInstanceOf(error);
    expect(getFlowRun).toHaveBeenCalledTimes(calls);
  });

  it("rejects with AbortError and stops polling when the signal aborts", async () => {
    const controller = new AbortController();
    const { getFlowRun, settled } = startWait([details(FlowRunStatus.RUNNING)], controller.signal);
    await vi.advanceTimersByTimeAsync(1500);

    controller.abort();
    await vi.advanceTimersByTimeAsync(60_000);

    expect((await settled).error).toBeInstanceOf(AbortError);
    expect(getFlowRun).toHaveBeenCalledTimes(2);
  });

  it("passes the flow run ID to getFlowRun", async () => {
    const { getFlowRun, settled } = startWait([details(FlowRunStatus.SUCCEEDED)]);

    await settled;

    expect(getFlowRun).toHaveBeenCalledWith("frn-1", expect.any(AbortSignal));
  });
});
