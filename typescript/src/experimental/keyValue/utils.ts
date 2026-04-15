export function isRender(): boolean {
  return process.env.RENDER === "true";
}

export function formatErrorMessage(failure: string, call_to_action: string): string {
  return `${failure}

${call_to_action}`;
}
