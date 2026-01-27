import type { Client } from "openapi-fetch";
import type { paths } from "../../generated/schema.js";
import { RenderError } from "../../errors.js";
import type {
  PutBlobInput,
  GetBlobInput,
  DeleteBlobInput,
  BlobData,
  PutBlobResult,
  BlobScope,
  ScopedPutBlobInput,
  ScopedGetBlobInput,
  ScopedDeleteBlobInput,
  Region,
} from "./types.js";

/**
 * Layer 3: High-Level Blob Client
 *
 * User-facing API that abstracts presigned URLs completely.
 * Provides simple put/get/delete operations that handle the
 * two-step presigned URL flow internally.
 */
export class BlobClient {
  constructor(private readonly apiClient: Client<paths>) {}

  /**
   * Upload a blob to storage
   *
   * @param input - Upload parameters including blob identifier and data
   * @returns Result with optional ETag
   *
   * @example
   * ```typescript
   * // Upload a Buffer
   * const data = Buffer.from("binary content");
   * await blobClient.put({
   *   ownerId: "tea-xxxxx",
   *   region: "oregon",
   *   key: "path/to/file.png",
   *   data,
   *   contentType: "image/png"
   * });
   *
   * // Upload from stream
   * const stream = createReadStream("/path/to/file.zip");
   * const stats = statSync("/path/to/file.zip");
   * await blobClient.put({
   *   ownerId: "tea-xxxxx",
   *   region: "oregon",
   *   key: "file.zip",
   *   data: stream,
   *   size: stats.size
   * });
   * ```
   */
  async put(input: PutBlobInput): Promise<PutBlobResult> {
    // Resolve and validate size
    const size = this.resolveSize(input);

    // Step 1: Get presigned upload URL from Render API
    const { data, error } = await this.apiClient.PUT(
      "/blobs/{ownerId}/{region}/{key}",
      {
        params: {
          path: {
            ownerId: input.ownerId,
            region: input.region as Region,
            key: input.key,
          },
        },
        body: { sizeBytes: size },
      },
    );

    if (error) {
      throw new RenderError(
        `Failed to get upload URL: ${error.message || "Unknown error"}`,
      );
    }

    // Step 2: Upload to storage via presigned URL
    const headers: Record<string, string> = {
      "Content-Length": size.toString(),
    };

    if (input.contentType) {
      headers["Content-Type"] = input.contentType;
    }

    const response = await fetch(data.url, {
      method: "PUT",
      headers,
      body: input.data,
      duplex: "half",
    });

    if (!response.ok) {
      throw new RenderError(
        `Upload failed: ${response.status} ${response.statusText}`,
      );
    }

    return {
      etag: response.headers.get("ETag") ?? undefined,
    };
  }

  /**
   * Download a blob from storage
   *
   * @param input - Download parameters including blob identifier
   * @returns Blob data with content
   *
   * @example
   * ```typescript
   * const blob = await blobClient.get({
   *   ownerId: "tea-xxxxx",
   *   region: "oregon",
   *   key: "path/to/file.png"
   * });
   *
   * console.log(blob.size);           // Size in bytes
   * console.log(blob.contentType);    // MIME type if available
   * // blob.data is a Buffer
   * ```
   */
  async get(input: GetBlobInput): Promise<BlobData> {
    // Step 1: Get presigned download URL from Render API
    const { data, error } = await this.apiClient.GET(
      "/blobs/{ownerId}/{region}/{key}",
      {
        params: {
          path: {
            ownerId: input.ownerId,
            region: input.region as Region,
            key: input.key,
          },
        },
      },
    );

    if (error) {
      throw new RenderError(
        `Failed to get download URL: ${error.message || "Unknown error"}`,
      );
    }

    // Step 2: Download from storage via presigned URL
    const response = await fetch(data.url);

    if (!response.ok) {
      throw new RenderError(
        `Download failed: ${response.status} ${response.statusText}`,
      );
    }

    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    return {
      data: buffer,
      size: buffer.byteLength,
      contentType: response.headers.get("Content-Type") ?? undefined,
    };
  }

  /**
   * Delete a blob from storage
   *
   * @param input - Delete parameters including blob identifier
   *
   * @example
   * ```typescript
   * await blobClient.delete({
   *   ownerId: "tea-xxxxx",
   *   region: "oregon",
   *   key: "path/to/file.png"
   * });
   * ```
   */
  async delete(input: DeleteBlobInput): Promise<void> {
    // DELETE goes directly to Render API (no presigned URL)
    const { error } = await this.apiClient.DELETE(
      "/blobs/{ownerId}/{region}/{key}",
      {
        params: {
          path: {
            ownerId: input.ownerId,
            region: input.region as Region,
            key: input.key,
          },
        },
      },
    );

    if (error) {
      throw new RenderError(
        `Failed to delete blob: ${error.message || "Unknown error"}`,
      );
    }
  }

  /**
   * Create a scoped blob client for a specific owner and region
   *
   * @param scope - Owner ID and region to scope operations to
   * @returns Scoped blob client that doesn't require ownerId/region on each call
   *
   * @example
   * ```typescript
   * const scoped = blobClient.scoped({
   *   ownerId: "tea-xxxxx",
   *   region: "oregon"
   * });
   *
   * // Subsequent calls only need the key
   * await scoped.put({ key: "file.png", data: buffer });
   * await scoped.get({ key: "file.png" });
   * await scoped.delete({ key: "file.png" });
   * ```
   */
  scoped(scope: BlobScope): ScopedBlobClient {
    return new ScopedBlobClient(this.apiClient, scope);
  }

  /**
   * Resolve and validate the size for a put operation
   *
   * - For Buffer/Uint8Array: auto-calculate size, validate if provided
   * - For streams/strings: require explicit size
   */
  private resolveSize(input: PutBlobInput): number {
    if (Buffer.isBuffer(input.data) || input.data instanceof Uint8Array) {
      const actualSize = input.data.byteLength;

      if (input.size !== undefined && input.size !== actualSize) {
        throw new RenderError(
          `Size mismatch: provided size ${input.size} does not match actual size ${actualSize}`,
        );
      }

      return actualSize;
    }

    // For Readable streams or strings, size must be provided
    if (input.size === undefined) {
      throw new RenderError(
        "Size is required for stream and string inputs. Provide the size parameter.",
      );
    }

    if (input.size <= 0) {
      throw new RenderError("Size must be a positive integer");
    }

    return input.size;
  }
}

/**
 * Scoped Blob Client
 *
 * Pre-configured client for a specific owner and region.
 * Eliminates the need to specify ownerId and region on every operation.
 */
export class ScopedBlobClient {
  private readonly blobClient: BlobClient;

  constructor(
    apiClient: Client<paths>,
    private readonly scope: BlobScope,
  ) {
    this.blobClient = new BlobClient(apiClient);
  }

  /**
   * Upload a blob to storage using scoped owner and region
   *
   * @param input - Upload parameters (key and data only)
   * @returns Result with optional ETag
   *
   * @example
   * ```typescript
   * const scoped = blobClient.scoped({ ownerId: "tea-xxxxx", region: "oregon" });
   * await scoped.put({
   *   key: "file.png",
   *   data: Buffer.from("content"),
   *   contentType: "image/png"
   * });
   * ```
   */
  async put(input: ScopedPutBlobInput): Promise<PutBlobResult> {
    return this.blobClient.put({
      ...this.scope,
      ...input,
    } as PutBlobInput);
  }

  /**
   * Download a blob from storage using scoped owner and region
   *
   * @param input - Download parameters (key only)
   * @returns Blob data with content
   *
   * @example
   * ```typescript
   * const scoped = blobClient.scoped({ ownerId: "tea-xxxxx", region: "oregon" });
   * const blob = await scoped.get({ key: "file.png" });
   * ```
   */
  async get(input: ScopedGetBlobInput): Promise<BlobData> {
    return this.blobClient.get({
      ...this.scope,
      ...input,
    } as GetBlobInput);
  }

  /**
   * Delete a blob from storage using scoped owner and region
   *
   * @param input - Delete parameters (key only)
   *
   * @example
   * ```typescript
   * const scoped = blobClient.scoped({ ownerId: "tea-xxxxx", region: "oregon" });
   * await scoped.delete({ key: "file.png" });
   * ```
   */
  async delete(input: ScopedDeleteBlobInput): Promise<void> {
    return this.blobClient.delete({
      ...this.scope,
      ...input,
    } as DeleteBlobInput);
  }
}
