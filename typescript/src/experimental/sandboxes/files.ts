import { randomUUID } from "node:crypto";
import { open, rename, rm } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

import { RenderError, SandboxDownloadError, SandboxDownloadTooLargeError } from "../../errors.js";
import type { SandboxCopyFromResult, SandboxDownload, SandboxDownloadOptions } from "./index.js";

export type DownloadLimit = { sandboxId: string; path: string; maxSizeBytes: number };

export function downloadLimit(
  sandboxId: string,
  path: string,
  maxSizeBytes: number | undefined,
  defaultMaxSizeBytes: number,
): DownloadLimit {
  if (maxSizeBytes === undefined) {
    return { sandboxId, path, maxSizeBytes: defaultMaxSizeBytes };
  }

  if (!Number.isSafeInteger(maxSizeBytes) || maxSizeBytes <= 0) {
    throw new RangeError("maxSizeBytes must be a positive integer");
  }

  return { sandboxId, path, maxSizeBytes };
}

export function toDownloadOptions(
  signalOrOptions?: AbortSignal | SandboxDownloadOptions,
): SandboxDownloadOptions {
  if (signalOrOptions instanceof AbortSignal) {
    return { signal: signalOrOptions };
  }

  return signalOrOptions ?? {};
}

export async function readLimitedBody(
  response: Response,
  limit: DownloadLimit,
): Promise<SandboxDownload["data"]> {
  const declared = declaredLength(response);
  if (declared > limit.maxSizeBytes) {
    await response.body?.cancel();
    throw downloadTooLarge(limit);
  }

  if (response.body === null) {
    return Buffer.alloc(0);
  }

  let data = Buffer.alloc(declared);
  let size = 0;
  for await (const chunk of response.body) {
    const needed = size + chunk.byteLength;
    if (needed > limit.maxSizeBytes) {
      throw downloadTooLarge(limit);
    }

    if (needed > data.byteLength) {
      data = grow(data, size, Math.min(Math.max(needed, data.byteLength * 2), limit.maxSizeBytes));
    }

    data.set(chunk, size);
    size = needed;
  }

  return data.subarray(0, size);
}

function declaredLength(response: Response): number {
  const contentLength = response.headers.get("Content-Length");
  const lengthCountsDecodedBytes = !response.headers.has("Content-Encoding");
  if (contentLength === null || !lengthCountsDecodedBytes) {
    return 0;
  }

  return Number(contentLength);
}

function grow(
  data: SandboxDownload["data"],
  size: number,
  capacity: number,
): SandboxDownload["data"] {
  const grown = Buffer.alloc(capacity);
  grown.set(data.subarray(0, size));

  return grown;
}

export async function saveLimitedBody(
  response: Response,
  localPath: string,
  limit: DownloadLimit,
): Promise<SandboxCopyFromResult> {
  const contentType = response.headers.get("Content-Type") ?? undefined;
  if (contentType?.startsWith("application/x-tar")) {
    await response.body?.cancel();
    throw new RenderError(
      `Sandbox ${limit.sandboxId} path ${limit.path} is a directory; copyFrom copies only files`,
    );
  }

  if (declaredLength(response) > limit.maxSizeBytes) {
    await response.body?.cancel();
    throw downloadTooLarge(limit);
  }

  const target = resolve(localPath);
  const partial = join(dirname(target), `.partial-${randomUUID()}`);
  try {
    const size = await writeLimitedBody(response.body, partial, limit);
    await rename(partial, target);

    return { localPath: target, size, contentType };
  } catch (err) {
    await rm(partial, { force: true });
    // cancel() rejects with the body's own error when the body already failed; err is the one to report.
    await response.body?.cancel().catch(() => {});

    const isFileSystemError = err instanceof Error && "syscall" in err;
    if (isFileSystemError) {
      throw new SandboxDownloadError(
        `Could not write sandbox ${limit.sandboxId} file ${limit.path} to ${target}: ${err.message}`,
        limit.sandboxId,
        limit.path,
        target,
        err,
      );
    }

    throw err;
  }
}

async function writeLimitedBody(
  body: Response["body"],
  filePath: string,
  limit: DownloadLimit,
): Promise<number> {
  const file = await open(filePath, "wx");
  try {
    let size = 0;
    for await (const chunk of body ?? []) {
      size += chunk.byteLength;
      if (size > limit.maxSizeBytes) {
        throw downloadTooLarge(limit);
      }

      await file.writeFile(chunk);
    }

    return size;
  } finally {
    await file.close();
  }
}

function downloadTooLarge({
  sandboxId,
  path,
  maxSizeBytes,
}: DownloadLimit): SandboxDownloadTooLargeError {
  return new SandboxDownloadTooLargeError(
    `Sandbox ${sandboxId} file ${path} exceeds the ${maxSizeBytes}-byte download limit (maxSizeBytes)`,
    sandboxId,
    path,
    maxSizeBytes,
  );
}
