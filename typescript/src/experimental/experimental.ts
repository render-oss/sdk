import type { Client } from "openapi-fetch";
import type { paths } from "../generated/schema.js";
import { BlobClient } from "./blob/client.js";

/**
 * ExperimentalClient provides access to experimental Render SDK features
 *
 * Features in this namespace may change or be removed without a migration plan.
 * When a feature stabilizes, it will be promoted to the main SDK namespace.
 *
 * @example
 * ```typescript
 * import { Render } from '@renderinc/sdk';
 *
 * const render = new Render();
 *
 * // Access experimental blob storage
 * await render.experimental.blob.put({
 *   ownerId: "tea-xxxxx",
 *   region: "oregon",
 *   key: "file.png",
 *   data: buffer
 * });
 * ```
 */
export class ExperimentalClient {
  /** Blob storage client for managing binary objects */
  public readonly blob: BlobClient;

  constructor(apiClient: Client<paths>) {
    this.blob = new BlobClient(apiClient);
  }
}
