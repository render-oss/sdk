/**
 * Standalone CRUD check for object storage.
 *
 * No test-framework dependency — reusable by pollinators / health probes.
 */

import { randomUUID } from "node:crypto";
import { RenderError } from "../../errors.js";
import type { ObjectClient } from "./client.js";

const RETRY_ATTEMPTS = 5;
const RETRY_INTERVAL_MS = 1000;

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Run a full PUT → LIST → GET → DELETE → verify-deletion cycle.
 *
 * @returns The key that was used (caller can use it for follow-up assertions).
 */
export async function objectStorageCrudCheck(
  client: ObjectClient,
  ownerId: `tea-${string}`,
  region: string,
): Promise<string> {
  const key = `e2e-test/${randomUUID()}/crud-test.txt`;
  const content = Buffer.from("hello from e2e");

  try {
    // --- PUT ---
    await client.put({
      ownerId,
      region,
      key,
      data: content,
    });

    // --- LIST (with retry — eventual consistency) ---
    let found = false;
    for (let attempt = 1; attempt <= RETRY_ATTEMPTS; attempt++) {
      const listResponse = await client.list({ ownerId, region });
      const match = listResponse.objects.find((o) => o.key === key);
      if (match) {
        if (match.size !== content.byteLength) {
          throw new Error(`LIST size mismatch: expected ${content.byteLength}, got ${match.size}`);
        }
        // lastModified should be recent (within 5 minutes)
        const age = Date.now() - match.lastModified.getTime();
        if (age > 5 * 60 * 1000) {
          throw new Error(`LIST lastModified too old: ${match.lastModified.toISOString()}`);
        }
        found = true;
        break;
      }
      if (attempt < RETRY_ATTEMPTS) {
        await sleep(RETRY_INTERVAL_MS);
      }
    }
    if (!found) {
      throw new Error(`Object ${key} not found in LIST after ${RETRY_ATTEMPTS} attempts`);
    }

    // --- GET ---
    const obj = await client.get({ ownerId, region, key });
    if (!obj.data.equals(content)) {
      throw new Error("GET data does not match uploaded content");
    }
    if (obj.size !== content.byteLength) {
      throw new Error(`GET size mismatch: expected ${content.byteLength}, got ${obj.size}`);
    }
    // --- DELETE ---
    await client.delete({ ownerId, region, key });

    // --- Verify deletion ---
    try {
      await client.get({ ownerId, region, key });
      throw new Error("GET after DELETE should have thrown");
    } catch (err) {
      if (!(err instanceof RenderError)) {
        throw err;
      }
      // Expected — object was deleted
    }

    return key;
  } catch (err) {
    // Best-effort cleanup on failure
    try {
      await client.delete({ ownerId, region, key });
    } catch {
      // swallow cleanup errors
    }
    throw err;
  }
}
