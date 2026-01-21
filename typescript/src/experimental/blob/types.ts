import type { Readable } from "node:stream";

/**
 * Supported regions for blob storage
 */
export type Region = "frankfurt" | "oregon" | "ohio" | "singapore" | "virginia";

/**
 * Base identifier for a blob object
 */
export interface BlobIdentifier {
  /** Owner ID (workspace team ID) in format tea-xxxxx */
  ownerId: `tea-${string}`;
  /** Region where the blob is stored */
  region: Region | string;
  /** Object key (path) for the blob */
  key: string;
}

/**
 * Base options for putting a blob
 */
interface PutBlobInputBase extends BlobIdentifier {
  /** MIME type of the content (optional, will be auto-detected if not provided) */
  contentType?: string;
}

/**
 * Put blob input for Buffer, Uint8Array, or string data
 * Size is optional and will be auto-calculated
 */
export interface PutBlobInputBuffer extends PutBlobInputBase {
  /** Binary data as Buffer, Uint8Array, or string */
  data: Buffer | Uint8Array | string;
  /** Size in bytes (optional, auto-calculated for Buffer/Uint8Array) */
  size?: number;
}

/**
 * Put blob input for readable streams
 * Size is required for streams
 */
export interface PutBlobInputStream extends PutBlobInputBase {
  /** Readable stream */
  data: Readable;
  /** Size in bytes (required for streams) */
  size: number;
}

/**
 * Input for uploading a blob
 * Discriminated union: size is optional for Buffer/Uint8Array, required for streams
 */
export type PutBlobInput = PutBlobInputBuffer | PutBlobInputStream;

/**
 * Input for downloading a blob
 */
export interface GetBlobInput extends BlobIdentifier {}

/**
 * Input for deleting a blob
 */
export interface DeleteBlobInput extends BlobIdentifier {}

/**
 * Presigned URL for uploading
 */
export interface PresignedUploadUrl {
  /** Presigned upload URL */
  url: string;
  /** Expiration timestamp */
  expiresAt: Date;
  /** Maximum size allowed for upload */
  maxSizeBytes: number;
}

/**
 * Presigned URL for downloading
 */
export interface PresignedDownloadUrl {
  /** Presigned download URL */
  url: string;
  /** Expiration timestamp */
  expiresAt: Date;
}

/**
 * Downloaded blob data
 */
export interface BlobData {
  /** Binary content */
  data: Buffer;
  /** MIME type if available */
  contentType?: string;
  /** Size in bytes */
  size: number;
}

/**
 * Result from uploading a blob
 */
export interface PutBlobResult {
  /** ETag from storage provider */
  etag?: string;
}

/**
 * Scope configuration for scoped blob client
 */
export interface BlobScope {
  /** Owner ID (workspace team ID) in format tea-xxxxx */
  ownerId: `tea-${string}`;
  /** Region where the blob is stored */
  region: Region | string;
}

/**
 * Scoped input for uploading a blob (without ownerId/region)
 */
export type ScopedPutBlobInput = Omit<PutBlobInput, keyof BlobScope>;

/**
 * Scoped input for downloading a blob (without ownerId/region)
 */
export type ScopedGetBlobInput = Omit<GetBlobInput, keyof BlobScope>;

/**
 * Scoped input for deleting a blob (without ownerId/region)
 */
export type ScopedDeleteBlobInput = Omit<DeleteBlobInput, keyof BlobScope>;
