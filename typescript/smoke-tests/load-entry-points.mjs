// Loads the built SDK through its package exports. CI runs this on Node 18, where Vitest cannot
// start, to catch syntax or Node APIs the oldest supported runtime lacks.
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const entryPoints = ["@renderinc/sdk", "@renderinc/sdk/workflows", "@renderinc/sdk/experimental"];

for (const entryPoint of entryPoints) {
  const imported = await import(entryPoint);
  const required = require(entryPoint);
  assert.ok(Object.keys(imported).length > 0, `${entryPoint} has no ESM exports`);
  assert.ok(Object.keys(required).length > 0, `${entryPoint} has no CommonJS exports`);
}

const REDIS_MODULE = /[\\/]node_modules[\\/](@redis|redis)[\\/]/;
const redisLoaded = () => Object.keys(require.cache).some((path) => REDIS_MODULE.test(path));

const { Render } = await import("@renderinc/sdk");
const render = new Render({ token: "smoke-test" });

// redis dominates the SDK's import time, so only keyValue.newClient() loads it.
assert.ok(!redisLoaded(), "importing the SDK loaded redis");
process.env.RENDER_USE_LOCAL_DEV = "true";
const client = await render.experimental.keyValue.newClient({ name: "smoke-test" });
assert.equal(typeof client.connect, "function", "newClient() did not return a redis client");
assert.ok(redisLoaded(), "newClient() did not load redis");

console.log(`Loaded ${entryPoints.length} entry points on Node ${process.versions.node}`);
