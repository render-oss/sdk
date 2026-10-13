import { inputQuery, markImportFinished, markSdkStarted } from "./startup.js";
import { run } from "./workflows/runner.js";

const DIGITS_RE = /^\d+$/;

vi.mock("./workflows/executor.js", () => ({
  TaskExecutor: class {
    executeTask = vi.fn().mockResolvedValue(undefined);
  },
}));

describe("sdk_started_at", () => {
  it("is recorded as nanoseconds since the epoch when run() is entered, once", async () => {
    expect(new URLSearchParams(inputQuery()).get("sdk_started_at")).toBeNull();

    const before = BigInt(Date.now()) * 1_000_000n - 5_000_000n;
    await run("/unused.sock");
    const first = new URLSearchParams(inputQuery()).get("sdk_started_at");
    expect(first).toMatch(DIGITS_RE);
    expect(BigInt(first as string)).toBeGreaterThanOrEqual(before);
    expect(BigInt(first as string)).toBeLessThanOrEqual(
      BigInt(Date.now()) * 1_000_000n + 5_000_000n,
    );

    markSdkStarted();
    expect(new URLSearchParams(inputQuery()).get("sdk_started_at")).toBe(first);
  });
});

describe("sdk_import_finished_at", () => {
  it("keeps the first entry point's value", () => {
    markImportFinished();
    const first = new URLSearchParams(inputQuery()).get("sdk_import_finished_at");
    expect(first).toMatch(DIGITS_RE);

    markImportFinished();
    expect(new URLSearchParams(inputQuery()).get("sdk_import_finished_at")).toBe(first);
  });
});
