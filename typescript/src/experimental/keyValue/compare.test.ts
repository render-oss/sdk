import { compareInstanceConfiguration } from "./compare";
import type { InstanceConfiguration, KeyValueDetail } from "./types";

describe("compareInstanceConfiguration", () => {
  const current: KeyValueDetail = {
    id: "red-abc",
    name: "test-redis",
    createdAt: "2026-04-01 00:01:02",
    updatedAt: "2026-04-01 01:02:03",
    status: "available",
    region: "oregon",
    owner: {
      id: "tea-abc",
      name: "Test Team",
      email: "no@no.com",
      type: "team",
    },
    plan: "free",
    options: {
      maxmemoryPolicy: "allkeys_lru",
    },
    ipAllowList: [
      {
        cidrBlock: "0.0.0.0/0",
        description: "Allow all traffic",
      },
    ],
    version: "8.9.2",
  };

  it("returns null if no desired values set explicitly", () => {
    const desired = {};

    expect(compareInstanceConfiguration(desired, current)).toBeNull();
  });

  it("returns null if desired values match exactly", () => {
    const desired: InstanceConfiguration = {
      plan: "free",
      maxmemoryPolicy: "allkeys_lru",
      ipAllowList: [
        {
          cidrBlock: "0.0.0.0/0",
          description: "Allow all traffic",
        },
      ],
    };

    expect(compareInstanceConfiguration(desired, current)).toBeNull();
  });

  it("returns diff if changes are needed", () => {
    const desired: InstanceConfiguration = {
      plan: "starter",
      maxmemoryPolicy: "noeviction",
      ipAllowList: [],
    };

    expect(compareInstanceConfiguration(desired, current)).toEqual({
      plan: "starter",
      maxmemoryPolicy: "noeviction",
      ipAllowList: [],
    });
  });

  it("returns partial diff if only some options changed", () => {
    const desired: InstanceConfiguration = {
      plan: "free",
      maxmemoryPolicy: "noeviction",
    };

    expect(compareInstanceConfiguration(desired, current)).toEqual({
      maxmemoryPolicy: "noeviction",
    });
  });

  it("only compares CIDR block and ignores description for IP Allow List diff", () => {
    const desired: InstanceConfiguration = {
      ipAllowList: [
        {
          cidrBlock: "0.0.0.0/0",
          description: "Different description shouldn't be a diff",
        },
      ],
    };

    expect(compareInstanceConfiguration(desired, current)).toBeNull();
  });

  it("handles net new entry in IP allowlist", () => {
    const desired: InstanceConfiguration = {
      ipAllowList: [
        {
          cidrBlock: "0.0.0.0/0",
          description: "Allow all traffic",
        },
        {
          cidrBlock: "127.0.0.0/0",
          description: "localhost",
        },
      ],
    };

    expect(compareInstanceConfiguration(desired, current)).toEqual({
      ipAllowList: desired.ipAllowList,
    });
  });
});
