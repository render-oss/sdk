import type { ErrorEvent } from "eventsource";
import { ClientError, ServerError } from "../errors.js";

export const getApiError = (error: any, response: Response, context: string): Error => {
  const statusCode = response.status;
  const errorMessage = `${context}: ${error}`;

  if (statusCode >= 500) {
    return new ServerError(errorMessage, statusCode, error);
  } else if (statusCode >= 400) {
    return new ClientError(errorMessage, statusCode, error);
  }
  return new ClientError(errorMessage, statusCode, error);
};

/**
 * Helper function to determine if an EventSource (or HTTP) error is connection related.
 * We return standard HTTP status codes from our API and `eventsource` has
 * a non-standard `code` property on it's `ErrorEvent` we can use to check the
 * returned HTTP status code.
 */
export const isConnectionError = (error?: ErrorEvent | number): boolean => {
  if (error) {
    const status = typeof error === "number" ? error : error.code;
    if (status !== undefined) {
      // 408 (Timeout) and 429 (Too Many Requests) are retriable/transient,
      // other 4xx errors are client errors and not connection related.
      if (status >= 400 && status < 500 && status !== 408 && status !== 429) {
        return false;
      }
    }
  }
  return true;
};
