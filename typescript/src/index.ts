// Must stay the first import: it records when SDK import began.
import { markImportFinished } from "./startup.js";

// Main Render SDK class

export * from "./errors.js";
// Experimental features - types only (instances accessed via render.experimental)
export type { ExperimentalClient } from "./experimental/index.js";
export {
  type Sandbox,
  type SandboxBuild,
  type SandboxBuildCreateInput,
  type SandboxBuildGetInput,
  type SandboxBuildSource,
  type SandboxBuildStatus,
  SandboxBuildsClient,
  type SandboxCreateInput,
  type SandboxDownload,
  type SandboxEgressRule,
  type SandboxExecEvent,
  SandboxExecStreamError,
  SandboxesClient,
  type SandboxGroup,
  type SandboxGroupListInput,
  type SandboxGroupWithCursor,
  type SandboxImage,
  type SandboxImageGetInput,
  type SandboxImageImportInput,
  type SandboxImageSource,
  type SandboxImageStatus,
  SandboxImagesClient,
  type SandboxNetworkPolicy,
  type SandboxPlan,
  type SandboxRegistryCredential,
  type SandboxRegistryCredentials,
  type SandboxSnapshot,
  type SandboxSnapshotCreateInput,
  type SandboxSnapshotDeleteInput,
  type SandboxSnapshotGetInput,
  type SandboxSnapshotKind,
  type SandboxSnapshotListInput,
  type SandboxSnapshotStatus,
  SandboxSnapshotsClient,
  type SandboxSnapshotWithCursor,
  type SandboxUploadContentType,
  type SandboxUploadData,
  type SandboxUploadOptions,
  type SandboxWaitOptions,
} from "./experimental/sandboxes/index.js";
export { Render } from "./render.js";
export { getUserAgent, VERSION } from "./version.js";

markImportFinished();
