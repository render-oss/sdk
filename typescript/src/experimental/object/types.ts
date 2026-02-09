import type { Readable } from "node:stream";

/**
 * Supported regions for object storage
 */
export type Region = "frankfurt" | "oregon" | "ohio" | "singapore" | "virginia";

/**
 * Base identifier for a storage object
 */
export interface ObjectIdentifier {
  /** Owner ID (workspace team ID) in format tea-xxxxx */
  ownerId: `tea-${string}`;
  /** Region where the object is stored */
  region: Region | string;
  /** Object key (path) for the object */
  key: string;
}

/**
 * Base options for putting an object
 */
interface PutObjectInputBase extends ObjectIdentifier {
  /** MIME type of the content (optional, will be auto-detected if not provided) */
  contentType?: string;
}

/**
 * Put object input for Buffer, Uint8Array, or string data
 * Size is optional and will be auto-calculated
 */
export interface PutObjectInputBuffer extends PutObjectInputBase {
  /** Binary data as Buffer, Uint8Array, or string */
  data: Buffer | Uint8Array | string;
  /** Size in bytes (optional, auto-calculated for Buffer/Uint8Array) */
  size?: number;
}

/**
 * Put object input for readable streams
 * Size is required for streams
 */
export interface PutObjectInputStream extends PutObjectInputBase {
  /** Readable stream */
  data: Readable;
  /** Size in bytes (required for streams) */
  size: number;
}

/**
 * Input for uploading an object
 * Discriminated union: size is optional for Buffer/Uint8Array, required for streams
 */
export type PutObjectInput = PutObjectInputBuffer | PutObjectInputStream;

/**
 * Input for downloading an object
 */
export interface GetObjectInput extends ObjectIdentifier {}

/**
 * Input for deleting an object
 */
export interface DeleteObjectInput extends ObjectIdentifier {}

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
 * Downloaded object data
 */
export interface ObjectData {
  /** Binary content */
  data: Buffer;
  /** MIME type if available */
  contentType?: string;
  /** Size in bytes */
  size: number;
}

/**
 * Result from uploading an object
 */
export interface PutObjectResult {
  /** ETag from storage provider */
  etag?: string;
}

/**
 * Scope configuration for scoped object client
 */
export interface ObjectScope {
  /** Owner ID (workspace team ID) in format tea-xxxxx */
  ownerId: `tea-${string}`;
  /** Region where the object is stored */
  region: Region | string;
}

/**
 * Scoped input for uploading an object (without ownerId/region)
 */
export type ScopedPutObjectInput = Omit<PutObjectInput, keyof ObjectScope>;

/**
 * Scoped input for downloading an object (without ownerId/region)
 */
export type ScopedGetObjectInput = Omit<GetObjectInput, keyof ObjectScope>;

/**
 * Scoped input for deleting an object (without ownerId/region)
 */
export type ScopedDeleteObjectInput = Omit<DeleteObjectInput, keyof ObjectScope>;

/**
 * Input for listing objects
 */
export interface ListObjectsInput {
  /** Owner ID (workspace team ID) in format tea-xxxxx */
  ownerId: `tea-${string}`;
  /** Region where the objects are stored */
  region: Region | string;
  /** Pagination cursor from previous response */
  cursor?: string;
  /** Maximum number of objects to return (default 20) */
  limit?: number;
}

/**
 * Scoped input for listing objects (without ownerId/region)
 */
export type ScopedListObjectsInput = Omit<ListObjectsInput, keyof ObjectScope>;

/**
 * Metadata for a stored object
 */
export interface ObjectMetadata {
  /** Object key (path) */
  key: string;
  /** Size in bytes */
  size: number;
  /** When the object was last modified */
  lastModified: Date;
}

/**
 * Response from listing objects
 */
export interface ListObjectsResponse {
  /** List of object metadata */
  objects: ObjectMetadata[];
  /** Cursor for next page, undefined if no more results */
  nextCursor?: string;
}
