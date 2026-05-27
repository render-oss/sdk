import { RenderError } from "../../errors";
import { createApiClient } from "../../utils/create-api-client";
import { getBaseUrl } from "../../utils/get-base-url";
import { isLocalDev } from "../../utils/is-local-dev";
import { WorkflowsClient } from "./client";
import type { ClientOptions } from "./types";

export function createWorkflowsClient(options?: ClientOptions): WorkflowsClient {
  const token = options?.token || process.env.RENDER_API_KEY || "";
  const baseUrl = getBaseUrl(options);
  if (!token && !isLocalDev(options)) {
    throw new RenderError(
      "API token is required. Provide it via options.token or RENDER_API_KEY environment variable.",
    );
  }
  const apiClient = createApiClient(baseUrl, token);
  return new WorkflowsClient(apiClient, baseUrl, token);
}
