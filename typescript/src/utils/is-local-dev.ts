interface IsLocalDevProps {
  useLocalDev?: boolean;
  localDevUrl?: string;
}

const TRUTHY_LOCAL_DEV_VALUES = new Set(["1", "t", "T", "true", "TRUE", "True"]);

/**
 * Determines whether the client should run in local dev mode.
 *
 * Local dev mode is enabled when:
 *   - options.useLocalDev is true, or
 *   - options.localDevUrl is set, or
 *   - RENDER_USE_LOCAL_DEV is one of "1", "t", "T", "true", "TRUE", "True", or
 *   - RENDER_LOCAL_DEV_URL is set.
 */
export function isLocalDev(options?: IsLocalDevProps): boolean {
  if (options?.useLocalDev !== undefined) {
    return options.useLocalDev;
  }
  if (options?.localDevUrl) {
    return true;
  }
  if (process.env.RENDER_LOCAL_DEV_URL) {
    return true;
  }
  const envValue = process.env.RENDER_USE_LOCAL_DEV;
  return envValue !== undefined && TRUTHY_LOCAL_DEV_VALUES.has(envValue);
}
