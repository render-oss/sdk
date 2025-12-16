import createClient, { type Client } from "openapi-fetch";
import type { paths } from "./schema";

export function createApiClient(baseUrl: string, token: string): Client<paths> {
  return createClient<paths>({
    baseUrl: `${baseUrl}/v1`,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
