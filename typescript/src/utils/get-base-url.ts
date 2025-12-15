interface GetBaseUrlProps {
  useLocalDev?: boolean;
  localDevUrl?: string;
  baseUrl?: string;
}
export function getBaseUrl(options?: GetBaseUrlProps): string {
  let baseUrl: string;
  const useLocalDev = options?.useLocalDev ?? process.env.RENDER_USE_LOCAL_DEV === "true";

  if (useLocalDev) {
    baseUrl = options?.localDevUrl || process.env.RENDER_LOCAL_DEV_URL || "http://localhost:8120";
  } else {
    baseUrl = options?.baseUrl || "https://api.render.com";
  }
  return baseUrl;
}
