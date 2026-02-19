import { Render } from "../../render.js";
import { objectStorageCrudCheck } from "./e2e-helpers.js";

const canRunE2E = Boolean(process.env.RENDER_API_KEY && process.env.RENDER_E2E_OWNER_ID);
const canRunPagination = canRunE2E && Boolean(process.env.RENDER_E2E_PAGINATION_OWNER_ID);

// ---------------------------------------------------------------------------
// CRUD tests
// ---------------------------------------------------------------------------
describe.skipIf(!canRunE2E)("ObjectClient E2E", () => {
  const ownerId = process.env.RENDER_E2E_OWNER_ID as `tea-${string}`;
  const region = process.env.RENDER_E2E_REGION || "oregon";
  let render: Render;

  beforeAll(() => {
    render = new Render({
      baseUrl: process.env.RENDER_BASE_URL || undefined,
    });
  });

  const keysToCleanup: string[] = [];

  afterAll(async () => {
    for (const key of keysToCleanup) {
      try {
        await render.experimental.storage.objects.delete({ ownerId, region, key });
      } catch {
        // swallow — best-effort cleanup
      }
    }
  });

  it("should complete a full CRUD cycle", async () => {
    await objectStorageCrudCheck(render.experimental.storage.objects, ownerId, region);
    // Key was already deleted inside the helper; no cleanup needed
  });

  it("should work via scoped() accessor", async () => {
    const scoped = render.experimental.storage.objects.scoped({ ownerId, region });
    const key = `e2e-test/${crypto.randomUUID()}/scoped-test.txt`;
    keysToCleanup.push(key);

    await scoped.put({ key, data: Buffer.from("scoped") });
    const obj = await scoped.get({ key });
    expect(obj.data.toString()).toBe("scoped");
    await scoped.delete({ key });

    // Remove from cleanup since we just deleted it
    const idx = keysToCleanup.indexOf(key);
    if (idx !== -1) keysToCleanup.splice(idx, 1);
  });
});

// ---------------------------------------------------------------------------
// Pagination tests (pre-seeded org)
// ---------------------------------------------------------------------------
describe.skipIf(!canRunPagination)("ObjectClient E2E — Pagination", () => {
  const ownerId = process.env.RENDER_E2E_PAGINATION_OWNER_ID as `tea-${string}`;
  const region = process.env.RENDER_E2E_REGION || "oregon";
  let render: Render;

  beforeAll(() => {
    render = new Render({
      baseUrl: process.env.RENDER_BASE_URL || undefined,
    });
  });

  it("should paginate through all objects", async () => {
    const objects = render.experimental.storage.objects;
    const pageSize = 2;
    let cursor: string | undefined;
    let totalObjects = 0;
    let pages = 0;

    do {
      const response = await objects.list({
        ownerId,
        region,
        limit: pageSize,
        cursor,
      });

      expect(response.objects.length).toBeGreaterThan(0);
      totalObjects += response.objects.length;
      pages++;
      cursor = response.hasNext ? response.nextCursor : undefined;
    } while (cursor);

    // Pre-seeded org should have enough objects to require multiple pages
    expect(totalObjects).toBeGreaterThan(pageSize);
    expect(pages).toBeGreaterThan(1);
  });
});
