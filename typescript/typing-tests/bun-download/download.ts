import type { SandboxDownload } from "@renderinc/sdk";

declare const downloaded: SandboxDownload;

Bun.gunzipSync(downloaded.data);
new Blob([downloaded.data]);
