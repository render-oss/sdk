import type { Client } from "openapi-fetch";
import type { paths } from "../generated/schema.js";
import { ObjectClient } from "./object/client.js";

/**
 * StorageClient provides access to experimental storage features
 *
 * @example
 * ```typescript
 * // Access object storage
 * await render.experimental.storage.objects.put({
 *   ownerId: "tea-xxxxx",
 *   region: "oregon",
 *   key: "file.png",
 *   data: buffer
 * });
 * ```
 */
export class StorageClient {
  /** Object storage client for managing binary objects */
  public readonly objects: ObjectClient;

  constructor(apiClient: Client<paths>, defaultOwnerId?: string, defaultRegion?: string) {
    this.objects = new ObjectClient(apiClient, defaultOwnerId, defaultRegion);
  }
}

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
 * // Access experimental object storage
 * await render.experimental.storage.objects.put({
 *   ownerId: "tea-xxxxx",
 *   region: "oregon",
 *   key: "file.png",
 *   data: buffer
 * });
 * ```
 */
export class ExperimentalClient {
  /** Storage client for managing storage features */
  public readonly storage: StorageClient;

  constructor(apiClient: Client<paths>, defaultOwnerId?: string, defaultRegion?: string) {
    this.storage = new StorageClient(apiClient, defaultOwnerId, defaultRegion);
  }
}
