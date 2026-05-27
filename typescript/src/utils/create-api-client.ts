import createClient, { type Client } from "openapi-fetch";
import type { paths } from "../generated/schema";
import { getUserAgent } from "../version.js";

export function createApiClient(baseUrl: string, token: string): Client<paths> {
  const headers: Record<string, string> = {
    "User-Agent": getUserAgent(),
  };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return createClient<paths>({
    baseUrl: `${baseUrl}/v1`,
    headers,
  });
}
