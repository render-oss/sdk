import type { Options, RedisConfig } from "./types";

describe("Options discriminated union", () => {
  it("accepts variant with serviceId", () => {
    const input: Options = {
      serviceId: "red-xyz",
      autoProvision: false,
    };
    expectTypeOf(input).toExtend<Options>();
  });

  it("accepts variant with name and ownerId", () => {
    const input: Options = {
      name: "redis-db",
      ownerId: "tea-abc",
      autoProvision: {},
    };
    expectTypeOf(input).toExtend<Options>();
  });
});

describe("RedisConfig parameter type", () => {
  it("does not accept 'url' property", () => {
    expectTypeOf({ url: "http://www.google.com" }).not.toMatchObjectType<RedisConfig>();
  });
});
