import { randomUUID } from "node:crypto";
import { ClientError, ServerError } from "../../errors.js";
import { Render } from "../../render.js";
import type { SandboxExecEvent } from "./index.js";

const sbxIdRegex = /^sbx-/;
const sbgIdRegex = /^sbg-/;

const EXEC_RETRY_ATTEMPTS = 50;
const EXEC_RETRY_DELAY_MS = 3000;

function isTransientExecError(err: unknown): boolean {
  return (
    (err instanceof ClientError || err instanceof ServerError) &&
    (err.statusCode === 404 || err.statusCode === 429 || err.statusCode === 503)
  );
}

async function openExecWithRetry(
  sandboxes: Render["experimental"]["sandboxes"],
  sandboxId: string,
  command: string,
  ownerId: `tea-${string}`,
): Promise<AsyncGenerator<SandboxExecEvent>> {
  for (let attempt = 0; attempt < EXEC_RETRY_ATTEMPTS; attempt++) {
    try {
      return await sandboxes.exec(sandboxId, command, ownerId);
    } catch (err) {
      if (!isTransientExecError(err) || attempt === EXEC_RETRY_ATTEMPTS - 1) {
        throw err;
      }
      await new Promise((resolve) => setTimeout(resolve, EXEC_RETRY_DELAY_MS));
    }
  }
  throw new Error("could not establish exec stream");
}

describe.skipIf(!process.env.RENDER_E2E_OWNER_ID)("SandboxesClient E2E", () => {
  const ownerId = process.env.RENDER_E2E_OWNER_ID as `tea-${string}`;

  let render: Render;

  beforeAll(() => {
    render = new Render({
      baseUrl: process.env.RENDER_BASE_URL || undefined,
    });
  });

  it("lists the workspace's sandbox groups", async () => {
    const groups = await render.experimental.sandboxes.listGroups({ ownerId });

    expect(groups.length).toBeGreaterThan(0);
    for (const { sandboxGroup, cursor } of groups) {
      expect(sandboxGroup.id).toMatch(sbgIdRegex);
      expect(sandboxGroup.ownerId).toBe(ownerId);
      expect(sandboxGroup.region).toBeTruthy();
      expect(typeof sandboxGroup.concurrencyLimit).toBe("number");
      expect(cursor).toBeTruthy();
    }
    expect(groups.some(({ sandboxGroup }) => sandboxGroup.isDefault)).toBe(true);
  });

  it("creates, lists, uses, and terminates a sandbox", async () => {
    const sandboxes = render.experimental.sandboxes;
    const sandbox = await sandboxes.create({ ownerId });
    try {
      expect(sandbox.id).toMatch(sbxIdRegex);
      // API create response hardcodes status to "creating" for now; readiness is
      // observed via exec retries rather than polling get().
      expect(sandbox.status).toBe("creating");

      const listedSandboxes = await sandboxes.list({ ownerId });
      expect(listedSandboxes.some(({ sandbox: listed }) => listed.id === sandbox.id)).toBe(true);

      const stream = await openExecWithRetry(sandboxes, sandbox.id, "echo hello", ownerId);

      const events = [];
      for await (const event of stream) {
        events.push(event);
      }

      const output = events.find((event) => event.type === "output");
      expect(output).toMatchObject({
        type: "output",
        stream: "stdout",
        data: "hello\n",
      });

      const exit = events[events.length - 1];
      expect(exit).toMatchObject({ type: "exit", exit_code: 0 });

      const filename = `sdk-e2e-${randomUUID()}.txt`;
      const path = `/tmp/${filename}`;
      const contents = Buffer.from("hello from the Render SDK");
      await sandboxes.upload(sandbox.id, path, contents, ownerId);

      const downloaded = await sandboxes.download(sandbox.id, path, ownerId);
      expect(downloaded.data).toEqual(contents);
    } finally {
      await sandboxes.terminate(sandbox.id, ownerId);
    }
  });
});
