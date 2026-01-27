import type { Client } from "openapi-fetch";
import { RenderError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import type { PresignedDownloadUrl, PresignedUploadUrl, Region } from "./types.js";

/**
 * Layer 2: Typed Blob API Client
 *
 * Provides idiomatic TypeScript wrapper around the raw OpenAPI client.
 * Handles presigned URL flow but still exposes the two-step nature
 * (get URL, then upload/download). Useful for advanced use cases
 * requiring fine-grained control.
 */
export class BlobApi {
  constructor(private readonly apiClient: Client<paths>) {}

  /**
   * Get a presigned URL for uploading a blob
   *
   * @param ownerId - Owner ID (workspace team ID)
   * @param region - Storage region
   * @param key - Object key (path)
   * @param sizeBytes - Size of the blob in bytes
   * @returns Presigned upload URL with expiration and size limit
   */
  async getUploadUrl(
    ownerId: string,
    region: Region | string,
    key: string,
    sizeBytes: number,
  ): Promise<PresignedUploadUrl> {
    const { data, error } = await this.apiClient.PUT("/blobs/{ownerId}/{region}/{key}", {
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
   * Get a presigned URL for downloading a blob
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
    const { data, error } = await this.apiClient.GET("/blobs/{ownerId}/{region}/{key}", {
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
   * Delete a blob
   *
   * @param ownerId - Owner ID (workspace team ID)
   * @param region - Storage region
   * @param key - Object key (path)
   */
  async delete(ownerId: string, region: Region | string, key: string): Promise<void> {
    const { error } = await this.apiClient.DELETE("/blobs/{ownerId}/{region}/{key}", {
      params: { path: { ownerId, region: region as Region, key } },
    });

    if (error) {
      throw new RenderError(`Failed to delete blob: ${error.message || "Unknown error"}`);
    }
  }
}
