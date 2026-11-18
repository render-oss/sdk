import type { SandboxDownload } from "@renderinc/sdk";
import { StepError } from "@renderinc/sdk/workflows";

declare const downloaded: SandboxDownload;

Bun.gunzipSync(downloaded.data);
new Blob([downloaded.data]);

const wireError = { name: "PaymentError", message: "declined" };
const stepError = new StepError(wireError);
const errorName: string = stepError.errorName;
const stepName: string | undefined = stepError.stepName;
const originalMessage: string = stepError.originalMessage;
const errorData: unknown = stepError.data;
new StepError(wireError, "charge");
void [errorName, stepName, originalMessage, errorData];
