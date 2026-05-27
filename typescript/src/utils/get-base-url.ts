import { isLocalDev } from "./is-local-dev.js";

interface GetBaseUrlProps {
  useLocalDev?: boolean;
  localDevUrl?: string;
  baseUrl?: string;
}
export function getBaseUrl(options?: GetBaseUrlProps): string {
  let baseUrl: string;

  if (isLocalDev(options)) {
    baseUrl = options?.localDevUrl || process.env.RENDER_LOCAL_DEV_URL || "http://localhost:8120";
  } else {
    baseUrl = options?.baseUrl || "https://api.render.com";
  }
  return baseUrl;
}
