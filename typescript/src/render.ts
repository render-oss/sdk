import type { Client } from "openapi-fetch";
import { WorkflowsClient } from "./workflows/client/index.js";
import type { ClientOptions } from "./workflows/client/types.js";
import type { paths } from "./utils/schema.js";
import { createApiClient } from "./utils/create-api-client.js";
import { getBaseUrl } from "./utils/get-base-url.js";
import { RenderError } from "./errors.js";

/**
 * Main Render SDK class providing access to all Render products
 */
export class Render {
  public readonly workflows: WorkflowsClient;

  private readonly apiClient: Client<paths>;

  /**
   * Create a new Render SDK instance
   * @param options Client configuration options
   */
  constructor(options?: ClientOptions) {
    const token = options?.token || process.env.RENDER_API_KEY;
    if (!token) {
      throw new RenderError(
        "API token is required. Provide it via options.token or RENDER_API_KEY environment variable.",
      );
    }
    const baseUrl = getBaseUrl(options);
    this.apiClient = createApiClient(baseUrl, token);
    this.workflows = new WorkflowsClient(this.apiClient, baseUrl, token);
  }
}
