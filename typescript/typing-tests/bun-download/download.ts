import type { SandboxDownload } from "@renderinc/sdk/experimental";

declare const downloaded: SandboxDownload;

Bun.gunzipSync(downloaded.data);
new Blob([downloaded.data]);
