import { isLocalDev } from "./is-local-dev.js";

describe("isLocalDev", () => {
  const originalEnv = process.env;

  beforeEach(() => {
    process.env = { ...originalEnv };
    delete process.env.RENDER_USE_LOCAL_DEV;
    delete process.env.RENDER_LOCAL_DEV_URL;
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it("returns false by default", () => {
    expect(isLocalDev()).toBe(false);
  });

  it("respects explicit useLocalDev=true option", () => {
    expect(isLocalDev({ useLocalDev: true })).toBe(true);
  });

  it("respects explicit useLocalDev=false option even if env is set", () => {
    process.env.RENDER_USE_LOCAL_DEV = "true";
    process.env.RENDER_LOCAL_DEV_URL = "http://localhost:7777";
    expect(isLocalDev({ useLocalDev: false })).toBe(false);
  });

  it("treats localDevUrl option as implicit dev mode", () => {
    expect(isLocalDev({ localDevUrl: "http://localhost:9000" })).toBe(true);
  });

  it("treats RENDER_LOCAL_DEV_URL env var as implicit dev mode", () => {
    process.env.RENDER_LOCAL_DEV_URL = "http://localhost:7777";
    expect(isLocalDev()).toBe(true);
  });

  it.each(["1", "t", "T", "true", "TRUE", "True"])(
    "accepts RENDER_USE_LOCAL_DEV=%s as truthy",
    (value) => {
      process.env.RENDER_USE_LOCAL_DEV = value;
      expect(isLocalDev()).toBe(true);
    },
  );

  it.each(["0", "false", "False", "no", "", "anything-else"])(
    "rejects RENDER_USE_LOCAL_DEV=%s",
    (value) => {
      process.env.RENDER_USE_LOCAL_DEV = value;
      expect(isLocalDev()).toBe(false);
    },
  );
});
