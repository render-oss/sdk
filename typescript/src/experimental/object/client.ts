import type { Client } from "openapi-fetch";
import { RenderError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import type {
  DeleteObjectInput,
  GetObjectInput,
  ListObjectsInput,
  ListObjectsResponse,
  ObjectData,
  ObjectMetadata,
  ObjectScope,
  PutObjectInput,
  PutObjectResult,
  Region,
  ScopedDeleteObjectInput,
  ScopedGetObjectInput,
  ScopedListObjectsInput,
  ScopedPutObjectInput,
} from "./types.js";

/**
 * Layer 3: High-Level Object Client
 *
 * User-facing API that abstracts presigned URLs completely.
 * Provides simple put/get/delete operations that handle the
 * two-step presigned URL flow internally.
 */
export class ObjectClient {
  constructor(private readonly apiClient: Client<paths>) {}

  /**
   * Upload an object to storage
   *
   * @param input - Upload parameters including object identifier and data
   * @returns Result with optional ETag
   *
   * @example
   * ```typescript
   * // Upload a Buffer
   * const data = Buffer.from("binary content");
   * await objectClient.put({
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
   * await objectClient.put({
   *   ownerId: "tea-xxxxx",
   *   region: "oregon",
   *   key: "file.zip",
   *   data: stream,
   *   size: stats.size
   * });
   * ```
   */
  async put(input: PutObjectInput): Promise<PutObjectResult> {
    // Resolve and validate size
    const size = this.resolveSize(input);

    // Step 1: Get presigned upload URL from Render API
    const { data, error } = await this.apiClient.PUT("/blobs/{ownerId}/{region}/{key}", {
      params: {
        path: {
          ownerId: input.ownerId,
          region: input.region as Region,
          key: input.key,
        },
      },
      body: { sizeBytes: size },
    });

    if (error) {
      throw new RenderError(`Failed to get upload URL: ${error.message || "Unknown error"}`);
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
      throw new RenderError(`Upload failed: ${response.status} ${response.statusText}`);
    }

    return {
      etag: response.headers.get("ETag") ?? undefined,
    };
  }

  /**
   * Download an object from storage
   *
   * @param input - Download parameters including object identifier
   * @returns Object data with content
   *
   * @example
   * ```typescript
   * const obj = await objectClient.get({
   *   ownerId: "tea-xxxxx",
   *   region: "oregon",
   *   key: "path/to/file.png"
   * });
   *
   * console.log(obj.size);           // Size in bytes
   * console.log(obj.contentType);    // MIME type if available
   * // obj.data is a Buffer
   * ```
   */
  async get(input: GetObjectInput): Promise<ObjectData> {
    // Step 1: Get presigned download URL from Render API
    const { data, error } = await this.apiClient.GET("/blobs/{ownerId}/{region}/{key}", {
      params: {
        path: {
          ownerId: input.ownerId,
          region: input.region as Region,
          key: input.key,
        },
      },
    });

    if (error) {
      throw new RenderError(`Failed to get download URL: ${error.message || "Unknown error"}`);
    }

    // Step 2: Download from storage via presigned URL
    const response = await fetch(data.url);

    if (!response.ok) {
      throw new RenderError(`Download failed: ${response.status} ${response.statusText}`);
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
   * Delete an object from storage
   *
   * @param input - Delete parameters including object identifier
   *
   * @example
   * ```typescript
   * await objectClient.delete({
   *   ownerId: "tea-xxxxx",
   *   region: "oregon",
   *   key: "path/to/file.png"
   * });
   * ```
   */
  async delete(input: DeleteObjectInput): Promise<void> {
    // DELETE goes directly to Render API (no presigned URL)
    const { error } = await this.apiClient.DELETE("/blobs/{ownerId}/{region}/{key}", {
      params: {
        path: {
          ownerId: input.ownerId,
          region: input.region as Region,
          key: input.key,
        },
      },
    });

    if (error) {
      throw new RenderError(`Failed to delete object: ${error.message || "Unknown error"}`);
    }
  }

  /**
   * List objects in storage
   *
   * @param input - List parameters including owner, region, and optional pagination
   * @returns List of object metadata with optional next cursor
   *
   * @example
   * ```typescript
   * // List first page
   * const response = await objectClient.list({
   *   ownerId: "tea-xxxxx",
   *   region: "oregon"
   * });
   *
   * for (const obj of response.objects) {
   *   console.log(`${obj.key}: ${obj.size} bytes`);
   * }
   *
   * // Get next page if available
   * if (response.nextCursor) {
   *   const nextPage = await objectClient.list({
   *     ownerId: "tea-xxxxx",
   *     region: "oregon",
   *     cursor: response.nextCursor
   *   });
   * }
   * ```
   */
  async list(input: ListObjectsInput): Promise<ListObjectsResponse> {
    const { data, error } = await this.apiClient.GET("/blobs/{ownerId}/{region}", {
      params: {
        path: {
          ownerId: input.ownerId,
          region: input.region as Region,
        },
        query: {
          cursor: input.cursor,
          limit: input.limit,
        },
      },
    });

    if (error) {
      throw new RenderError(`Failed to list objects: ${error.message || "Unknown error"}`);
    }

    const objects: ObjectMetadata[] = data.map((item) => ({
      key: item.blob.key,
      size: item.blob.sizeBytes,
      lastModified: new Date(item.blob.lastModified),
      contentType: item.blob.contentType,
    }));

    // The cursor for the next page is the cursor of the last item
    const nextCursor = data.length > 0 ? data[data.length - 1].cursor : undefined;

    return { objects, nextCursor };
  }

  /**
   * Create a scoped object client for a specific owner and region
   *
   * @param scope - Owner ID and region to scope operations to
   * @returns Scoped object client that doesn't require ownerId/region on each call
   *
   * @example
   * ```typescript
   * const scoped = objectClient.scoped({
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
  scoped(scope: ObjectScope): ScopedObjectClient {
    return new ScopedObjectClient(this.apiClient, scope);
  }

  /**
   * Resolve and validate the size for a put operation
   *
   * - For Buffer/Uint8Array: auto-calculate size, validate if provided
   * - For streams/strings: require explicit size
   */
  private resolveSize(input: PutObjectInput): number {
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
 * Scoped Object Client
 *
 * Pre-configured client for a specific owner and region.
 * Eliminates the need to specify ownerId and region on every operation.
 */
export class ScopedObjectClient {
  private readonly objectClient: ObjectClient;

  constructor(
    apiClient: Client<paths>,
    private readonly scope: ObjectScope,
  ) {
    this.objectClient = new ObjectClient(apiClient);
  }

  /**
   * Upload an object to storage using scoped owner and region
   *
   * @param input - Upload parameters (key and data only)
   * @returns Result with optional ETag
   *
   * @example
   * ```typescript
   * const scoped = objectClient.scoped({ ownerId: "tea-xxxxx", region: "oregon" });
   * await scoped.put({
   *   key: "file.png",
   *   data: Buffer.from("content"),
   *   contentType: "image/png"
   * });
   * ```
   */
  async put(input: ScopedPutObjectInput): Promise<PutObjectResult> {
    return this.objectClient.put({
      ...this.scope,
      ...input,
    } as PutObjectInput);
  }

  /**
   * Download an object from storage using scoped owner and region
   *
   * @param input - Download parameters (key only)
   * @returns Object data with content
   *
   * @example
   * ```typescript
   * const scoped = objectClient.scoped({ ownerId: "tea-xxxxx", region: "oregon" });
   * const obj = await scoped.get({ key: "file.png" });
   * ```
   */
  async get(input: ScopedGetObjectInput): Promise<ObjectData> {
    return this.objectClient.get({
      ...this.scope,
      ...input,
    } as GetObjectInput);
  }

  /**
   * Delete an object from storage using scoped owner and region
   *
   * @param input - Delete parameters (key only)
   *
   * @example
   * ```typescript
   * const scoped = objectClient.scoped({ ownerId: "tea-xxxxx", region: "oregon" });
   * await scoped.delete({ key: "file.png" });
   * ```
   */
  async delete(input: ScopedDeleteObjectInput): Promise<void> {
    return this.objectClient.delete({
      ...this.scope,
      ...input,
    } as DeleteObjectInput);
  }

  /**
   * List objects in storage using scoped owner and region
   *
   * @param input - List parameters (cursor and limit only)
   * @returns List of object metadata with optional next cursor
   *
   * @example
   * ```typescript
   * const scoped = objectClient.scoped({ ownerId: "tea-xxxxx", region: "oregon" });
   * const response = await scoped.list();
   * for (const obj of response.objects) {
   *   console.log(`${obj.key}: ${obj.size} bytes`);
   * }
   * ```
   */
  async list(input: ScopedListObjectsInput = {}): Promise<ListObjectsResponse> {
    return this.objectClient.list({
      ...this.scope,
      ...input,
    } as ListObjectsInput);
  }
}
