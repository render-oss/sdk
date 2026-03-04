import type { Client } from "openapi-fetch";
import type { paths } from "../../generated/schema.js";
import { throwObjectApiError } from "./errors.js";
import type {
  ListObjectsResponse,
  ObjectMetadata,
  PresignedDownloadUrl,
  PresignedUploadUrl,
  Region,
} from "./types.js";

/**
 * Typed Object API Client
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
    const { data, error, response } = await this.apiClient.PUT(
      "/objects/{ownerId}/{region}/{key}",
      {
        params: { path: { ownerId, region: region as Region, key } },
        body: { sizeBytes },
      },
    );

    if (error) {
      throwObjectApiError("Failed to get upload URL", response, error);
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
    const { data, error, response } = await this.apiClient.GET(
      "/objects/{ownerId}/{region}/{key}",
      {
        params: { path: { ownerId, region: region as Region, key } },
      },
    );

    if (error) {
      throwObjectApiError("Failed to get download URL", response, error);
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
    const { error, response } = await this.apiClient.DELETE("/objects/{ownerId}/{region}/{key}", {
      params: { path: { ownerId, region: region as Region, key } },
    });

    if (error) {
      throwObjectApiError("Failed to delete object", response, error);
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
    const { data, error, response } = await this.apiClient.GET("/objects/{ownerId}/{region}", {
      params: {
        path: { ownerId, region: region as Region },
        query: { cursor, limit },
      },
    });

    if (error) {
      throwObjectApiError("Failed to list objects", response, error);
    }

    const objects: ObjectMetadata[] = data.items.map((item) => ({
      key: item.object.key,
      size: item.object.sizeBytes,
      lastModified: new Date(item.object.lastModified),
    }));

    return { objects, hasNext: data.hasNext, nextCursor: data.nextCursor };
  }
}
