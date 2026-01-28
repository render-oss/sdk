import { getBaseUrl } from "./get-base-url.js";

describe("getBaseUrl", () => {
  const originalEnv = process.env;

  beforeEach(() => {
    process.env = { ...originalEnv };
    process.env.RENDER_USE_LOCAL_DEV = undefined;
    process.env.RENDER_LOCAL_DEV_URL = undefined;
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it("returns production URL by default", () => {
    expect(getBaseUrl()).toBe("https://api.render.com");
  });

  it("returns custom baseUrl when provided", () => {
    expect(getBaseUrl({ baseUrl: "https://custom.api.com" })).toBe("https://custom.api.com");
  });

  it("returns local dev URL when useLocalDev is true", () => {
    expect(getBaseUrl({ useLocalDev: true })).toBe("http://localhost:8120");
  });

  it("respects custom localDevUrl", () => {
    expect(getBaseUrl({ useLocalDev: true, localDevUrl: "http://localhost:9000" })).toBe(
      "http://localhost:9000",
    );
  });

  it("respects RENDER_USE_LOCAL_DEV env var", () => {
    process.env.RENDER_USE_LOCAL_DEV = "true";
    expect(getBaseUrl()).toBe("http://localhost:8120");
  });

  it("respects RENDER_LOCAL_DEV_URL env var", () => {
    process.env.RENDER_USE_LOCAL_DEV = "true";
    process.env.RENDER_LOCAL_DEV_URL = "http://localhost:7777";
    expect(getBaseUrl()).toBe("http://localhost:7777");
  });

  it("option overrides env var for localDevUrl", () => {
    process.env.RENDER_USE_LOCAL_DEV = "true";
    process.env.RENDER_LOCAL_DEV_URL = "http://localhost:7777";
    expect(getBaseUrl({ useLocalDev: true, localDevUrl: "http://localhost:9999" })).toBe(
      "http://localhost:9999",
    );
  });

  it("ignores baseUrl option when in local dev mode", () => {
    expect(getBaseUrl({ useLocalDev: true, baseUrl: "https://custom.api.com" })).toBe(
      "http://localhost:8120",
    );
  });
});
