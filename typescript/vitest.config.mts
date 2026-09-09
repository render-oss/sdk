import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["src/**/*.test.ts"],
    exclude: ["src/**/*.e2e.test.ts"],
    globals: true,
    fsModuleCache: true,
  },
});
