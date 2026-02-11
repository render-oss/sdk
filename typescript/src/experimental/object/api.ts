import type { Client } from "openapi-fetch";
import { RenderError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import type {
  ListObjectsResponse,
  ObjectMetadata,
  PresignedDownloadUrl,
  PresignedUploadUrl,
  Region,
} from "./types.js";

/**
 * Layer 2: Typed Object API Client
 *
 * Provides idiomatic TypeScript wrapper around the raw OpenAPI client.
 * Handles presigned URL flow but still exposes the two-step nature
 * (get URL, then upload/download). Useful for advanced use cases
 * requiring fine-grained control.
 */
export class ObjectApi {
  constructor(private readonly apiClient: Client<paths>) {}

  /**
   * Get a presigned URL for uploading an object
   *
   * @param ownerId - Owner ID (workspace team ID)
   * @param region - Storage region
   * @param key - Object key (path)
   * @param sizeBytes - Size of the object in bytes
   * @returns Presigned upload URL with expiration and size limit
   */
  async getUploadUrl(
    ownerId: string,
    region: Region | string,
    key: string,
    sizeBytes: number,
  ): Promise<PresignedUploadUrl> {
    const { data, error } = await this.apiClient.PUT("/objects/{ownerId}/{region}/{key}", {
      params: { path: { ownerId, region: region as Region, key } },
      body: { sizeBytes },
    });

    if (error) {
      throw new RenderError(`Failed to get upload URL: ${error.message || "Unknown error"}`);
    }

    return {
      url: data.url,
      expiresAt: new Date(data.expiresAt),
      maxSizeBytes: data.maxSizeBytes,
    };
  }

  /**
   * Get a presigned URL for downloading an object
   *
   * @param ownerId - Owner ID (workspace team ID)
   * @param region - Storage region
   * @param key - Object key (path)
   * @returns Presigned download URL with expiration
   */
  async getDownloadUrl(
    ownerId: string,
    region: Region | string,
    key: string,
  ): Promise<PresignedDownloadUrl> {
    const { data, error } = await this.apiClient.GET("/objects/{ownerId}/{region}/{key}", {
      params: { path: { ownerId, region: region as Region, key } },
    });

    if (error) {
      throw new RenderError(`Failed to get download URL: ${error.message || "Unknown error"}`);
    }

    return {
      url: data.url,
      expiresAt: new Date(data.expiresAt),
    };
  }

  /**
   * Delete an object
   *
   * @param ownerId - Owner ID (workspace team ID)
   * @param region - Storage region
   * @param key - Object key (path)
   */
  async delete(ownerId: string, region: Region | string, key: string): Promise<void> {
    const { error } = await this.apiClient.DELETE("/objects/{ownerId}/{region}/{key}", {
      params: { path: { ownerId, region: region as Region, key } },
    });

    if (error) {
      throw new RenderError(`Failed to delete object: ${error.message || "Unknown error"}`);
    }
  }

  /**
   * List objects in storage
   *
   * @param ownerId - Owner ID (workspace team ID)
   * @param region - Storage region
   * @param cursor - Pagination cursor from previous response
   * @param limit - Maximum number of objects to return (default 20)
   * @returns List of object metadata with optional next cursor
   */
  async listObjects(
    ownerId: string,
    region: Region | string,
    cursor?: string,
    limit?: number,
  ): Promise<ListObjectsResponse> {
    const { data, error } = await this.apiClient.GET("/objects/{ownerId}/{region}", {
      params: {
        path: { ownerId, region: region as Region },
        query: { cursor, limit },
      },
    });

    if (error) {
      throw new RenderError(`Failed to list objects: ${error.message || "Unknown error"}`);
    }

    const objects: ObjectMetadata[] = data.items.map((item) => ({
      key: item.object.key,
      size: item.object.sizeBytes,
      lastModified: new Date(item.object.lastModified),
    }));

    return { objects, hasNext: data.hasNext, nextCursor: data.nextCursor };
  }
}
