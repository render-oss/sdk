import { ClientError, ServerError } from "../../errors.js";

function errorDetailForStatus(status: number): string {
  if (status === 400) return "bad request";
  if (status === 401) return "authentication required";
  if (status === 403) return "access denied";
  if (status === 404) return "object not found";
  if (status === 409) return "conflict";
  if (status === 413) return "object too large";
  if (status === 429) return "rate limited, please try again later";
  if (status >= 500) return "storage service temporarily unavailable";
  return "unexpected error";
}

/**
 * Throws a typed error for a failed Render API call (e.g. getting a presigned URL).
 * Uses the error body message when available, otherwise falls back to a safe status-based message.
 * The original error body is preserved in the thrown error's `response` field.
 */
export function throwObjectApiError(
  operation: string,
  response: Response,
  error: { message?: string },
): never {
  const status = response.status;
  const detail = error.message ?? errorDetailForStatus(status);
  const message = `${operation} with status ${status}: ${detail}`;
  if (status >= 500) throw new ServerError(message, status, error);
  throw new ClientError(message, status, error);
}

/**
 * Throws a typed error for a failed direct storage request (e.g. PUT/GET to a presigned URL).
 * Uses sanitized status-based messages to avoid leaking raw XML responses from storage backends.
 */
export function throwStorageError(operation: string, response: Response): never {
  const status = response.status;
  const detail = errorDetailForStatus(status);
  const message = `${operation} with status ${status}: ${detail}`;
  if (status >= 500) throw new ServerError(message, status);
  throw new ClientError(message, status);
}
