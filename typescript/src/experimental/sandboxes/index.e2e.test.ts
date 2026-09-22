import { randomUUID } from "node:crypto";
import { ClientError, ServerError } from "../../errors.js";
import { Render } from "../../render.js";
import type { Sandbox, SandboxExecEvent, SandboxSnapshot } from "./index.js";

const sbxIdRegex = /^sbx-/;
const sbgIdRegex = /^sbg-/;

const EXEC_RETRY_ATTEMPTS = 50;
const EXEC_RETRY_DELAY_MS = 3000;
const RESOURCE_RETRY_ATTEMPTS = 90;
const RESOURCE_RETRY_DELAY_MS = 2000;

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

async function waitUntilSnapshotAvailable(
  sandboxes: Render["experimental"]["sandboxes"],
  snapshot: SandboxSnapshot,
  ownerId: `tea-${string}`,
): Promise<SandboxSnapshot> {
  for (let attempt = 0; attempt < RESOURCE_RETRY_ATTEMPTS; attempt++) {
    const current = await sandboxes.snapshots.get({
      sandboxGroupId: snapshot.sandboxGroupId,
      snapshotId: snapshot.id,
      ownerId,
    });
    if (current.status === "available") return current;
    if (current.status === "failed") {
      throw new Error(`snapshot ${snapshot.id} failed: ${current.error}`);
    }
    await new Promise((resolve) => setTimeout(resolve, RESOURCE_RETRY_DELAY_MS));
  }
  throw new Error(`snapshot ${snapshot.id} did not become available`);
}

async function execOutput(
  sandboxes: Render["experimental"]["sandboxes"],
  sandboxId: string,
  command: string,
  ownerId: `tea-${string}`,
): Promise<string> {
  const stream = await openExecWithRetry(sandboxes, sandboxId, command, ownerId);
  const output: string[] = [];
  let exitCode: number | undefined;
  for await (const event of stream) {
    if (event.type === "output" && event.stream === "stdout") output.push(event.data);
    if (event.type === "exit") exitCode = event.exit_code;
  }
  if (exitCode !== 0) throw new Error(`${command} exited ${exitCode}`);
  return output.join("");
}

describe.skipIf(!process.env.RENDER_E2E_OWNER_ID)("SandboxesClient E2E", () => {
  const ownerId = process.env.RENDER_E2E_OWNER_ID as `tea-${string}`;

  let render: Render;

  beforeAll(() => {
    render = new Render({
      baseUrl: process.env.RENDER_BASE_URL || undefined,
    });
  });

  describe("groups", () => {
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
  });

  describe("sandboxes", () => {
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
  describe("snapshots", () => {
    it("creates a filesystem snapshot", async () => {
      const sandboxes = render.experimental.sandboxes;
      const sandbox = await sandboxes.create({ ownerId });
      let snapshot: SandboxSnapshot | null = null;
      try {
        await execOutput(sandboxes, sandbox.id, "true", ownerId);
        snapshot = await sandboxes.snapshots.create({ sandboxId: sandbox.id, kind: "filesystem" });
        snapshot = await waitUntilSnapshotAvailable(sandboxes, snapshot, ownerId);
        expect(snapshot.status).toBe("available");
        expect(snapshot.error).toBeFalsy();
      } finally {
        await Promise.all([
          sandboxes.terminate(sandbox.id, ownerId),
          snapshot
            ? sandboxes.snapshots.delete({
                ownerId,
                snapshotId: snapshot.id,
                sandboxGroupId: snapshot.sandboxGroupId,
              })
            : Promise.resolve(),
        ]);
      }
    });
    it("restores a sandbox from a named snapshot", async () => {
      const sandboxes = render.experimental.sandboxes;
      const sandbox = await sandboxes.create({ ownerId });
      const name = `sdk-e2e-${randomUUID()}`;
      const marker = `marker-${randomUUID()}`;
      let snapshot: SandboxSnapshot | null = null;
      let restored: Sandbox | null = null;
      try {
        await execOutput(sandboxes, sandbox.id, `printf ${marker} > /tmp/marker`, ownerId);

        snapshot = await sandboxes.snapshots.create({
          sandboxId: sandbox.id,
          kind: "filesystem",
          name,
          ownerId,
        });
        snapshot = await waitUntilSnapshotAvailable(sandboxes, snapshot, ownerId);
        expect(snapshot.status).toBe("available");
        expect(snapshot.error).toBeFalsy();
        expect(snapshot.name).toBe(name);

        const listed = await sandboxes.snapshots.list({
          sandboxGroupId: snapshot.sandboxGroupId,
          ownerId,
        });
        expect(
          listed.some(({ snapshot: item }) => item.id === snapshot?.id && item.name === name),
        ).toBe(true);

        restored = await sandboxes.create({ ownerId, snapshotName: name });
        expect(await execOutput(sandboxes, restored.id, "cat /tmp/marker", ownerId)).toBe(marker);
      } finally {
        await Promise.all([
          sandboxes.terminate(sandbox.id, ownerId),
          restored ? sandboxes.terminate(restored.id, ownerId) : Promise.resolve(),
          snapshot
            ? sandboxes.snapshots.delete({
                ownerId,
                snapshotId: snapshot.id,
                sandboxGroupId: snapshot.sandboxGroupId,
              })
            : Promise.resolve(),
        ]);
      }
    });
  });
});
