// Wall-clock startup timestamps reported to the server on GET /input.
// Keep this module dependency-free and import it first from every package
// entry point, so the import start is recorded before any other SDK code runs.

function nowNs(): string | undefined {
  try {
    const ms = performance.timeOrigin + performance.now();
    return BigInt(Math.round(ms * 1e6)).toString();
  } catch {
    return undefined;
  }
}

const importStarted = nowNs();
let importFinished: string | undefined;
let sdkStarted: string | undefined;

/** Called at the end of each entry point; the first call wins. */
export function markImportFinished(): void {
  importFinished ??= nowNs();
}

export function markSdkStarted(): void {
  sdkStarted ??= nowNs();
}

/** Returns `?k=v&...` for the timestamps that were captured, or `""`. */
export function inputQuery(): string {
  const params: Array<[string, string | undefined]> = [
    ["sdk_import_started_at", importStarted],
    ["sdk_import_finished_at", importFinished],
    ["sdk_started_at", sdkStarted],
  ];
  const parts = params.flatMap(([name, value]) => (value ? [`${name}=${value}`] : []));
  return parts.length > 0 ? `?${parts.join("&")}` : "";
}
