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

const { Render } = await import("@renderinc/sdk");
new Render({ token: "smoke-test" });

console.log(`Loaded ${entryPoints.length} entry points on Node ${process.versions.node}`);
