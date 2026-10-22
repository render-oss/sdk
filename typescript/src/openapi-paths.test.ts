import fs from "node:fs";
import path from "node:path";

// openapi-paths.json lists the REST paths this SDK calls. The generator in
// renderinc/api (public-api-schema/generate-sdk.sh) filters the public API
// schema to those paths before emitting src/generated/schema.ts, so the npm
// package only ships types the SDK can reach.
//
// These tests keep the list honest: every path the source calls must be in
// it, and every entry must exist in the schema. The list may be a superset of
// what the source calls, because adding an endpoint means listing it here and
// regenerating before the code that uses it can typecheck.

const root = path.resolve(__dirname, "..");
const allowlistFile = path.join(root, "openapi-paths.json");
const schemaFile = path.join(root, "src/generated/schema.ts");

const PATHS_REF = /paths\["([^"]+)"\]/g;
const FETCH_CALL = /\.(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\(\s*"([^"]+)"/g;
const IMPORTS_SCHEMA = /from "[./]*\/generated\/schema(?:\.js)?"/;
const SOURCE_FILE = /\.m?ts$/;
const TEST_FILE = /\.test\.m?ts$/;
const SCHEMA_PATH_KEY = /^ {4}"(\/[^"]*)": \{$/gm;

function pathsCalledInSource(): Set<string> {
  const found = new Set<string>();
  const walk = (dir: string) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (entry.name !== "generated") walk(p);
        continue;
      }
      if (!SOURCE_FILE.test(entry.name) || TEST_FILE.test(entry.name)) continue;
      const text = fs.readFileSync(p, "utf8");
      // src/workflows/schema.ts is a different generated schema; only files
      // that import the public API schema count.
      if (!IMPORTS_SCHEMA.test(text)) continue;
      for (const m of text.matchAll(PATHS_REF)) found.add(m[1]);
      for (const m of text.matchAll(FETCH_CALL)) found.add(m[1]);
    }
  };
  walk(path.join(root, "src"));
  return found;
}

describe("openapi-paths.json", () => {
  const allowlist = JSON.parse(fs.readFileSync(allowlistFile, "utf8")) as { paths: string[] };
  const schema = fs.readFileSync(schemaFile, "utf8");

  it("has the expected shape", () => {
    expect(Object.keys(allowlist).sort()).toEqual(["$comment", "paths"]);
    expect(allowlist.paths.length).toBeGreaterThan(0);
  });

  it("is sorted with no duplicates", () => {
    expect(allowlist.paths).toEqual([...new Set(allowlist.paths)].sort());
  });

  it("lists every path the source calls", () => {
    const called = [...pathsCalledInSource()].sort();
    expect(called.length).toBeGreaterThan(0);
    const missing = called.filter((p) => !allowlist.paths.includes(p));
    expect(missing, "add these to openapi-paths.json and regenerate").toEqual([]);
  });

  it("only lists paths the generated schema defines", () => {
    const defined = new Set([...schema.matchAll(SCHEMA_PATH_KEY)].map((m) => m[1]));
    const unknown = allowlist.paths.filter((p) => !defined.has(p));
    expect(unknown, "not in src/generated/schema.ts").toEqual([]);
  });
});
