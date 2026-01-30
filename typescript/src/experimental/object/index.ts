// Object storage client exports
export { ObjectApi } from "./api.js";
export { ObjectClient, ScopedObjectClient } from "./client.js";
// Type exports
export type {
  DeleteObjectInput,
  GetObjectInput,
  ListObjectsInput,
  ListObjectsResponse,
  ObjectData,
  ObjectIdentifier,
  ObjectMetadata,
  ObjectScope,
  PresignedDownloadUrl,
  PresignedUploadUrl,
  PutObjectInput,
  PutObjectInputBuffer,
  PutObjectInputStream,
  PutObjectResult,
  ScopedDeleteObjectInput,
  ScopedGetObjectInput,
  ScopedListObjectsInput,
  ScopedPutObjectInput,
} from "./types.js";
// Re-export the Region enum (both type and value)
export { Region } from "./types.js";
