import { RenderError } from "../../errors";
import { createApiClient } from "../../utils/create-api-client";
import { getBaseUrl } from "../../utils/get-base-url";
import { WorkflowsClient } from "./client";
import type { ClientOptions } from "./types";

export function createWorkflowsClient(options?: ClientOptions): WorkflowsClient {
  const token = options?.token || process.env.RENDER_API_KEY;
  if (!token) {
    throw new RenderError(
      "API token is required. Provide it via options.token or RENDER_API_KEY environment variable.",
    );
  }
  const baseUrl = getBaseUrl(options);
  const apiClient = createApiClient(baseUrl, token);
  return new WorkflowsClient(apiClient, baseUrl, token);
}
