/**
 * Version information for the Render SDK.
 */

import { readFileSync } from "node:fs";
import { join } from "node:path";

/**
 * Get the SDK version from package.json.
 * __dirname points to dist/ after compilation, package.json is one level up.
 */
function getVersion(): string {
  try {
    const pkgPath = join(__dirname, "..", "package.json");
    const pkg = JSON.parse(readFileSync(pkgPath, "utf-8")) as { version?: string };
    return pkg.version ?? "unknown";
  } catch {
    return "unknown";
  }
}

/** The current version of the Render TypeScript SDK. */
export const VERSION = getVersion();

/**
 * Get the User-Agent string for the SDK.
 *
 * Returns a string like:
 *   render-sdk-typescript/0.1.0 (node/20.10.0; darwin/arm64)
 */
export function getUserAgent(): string {
  const nodeVersion = process.version.replace("v", "");
  const platform = process.platform;
  const arch = process.arch;

  return `render-sdk-typescript/${VERSION} (node/${nodeVersion}; ${platform}/${arch})`;
}
