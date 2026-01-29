import type { Readable } from "node:stream";
import type {
  DeleteObjectInput,
  GetObjectInput,
  ObjectIdentifier,
  ObjectScope,
  PutObjectInput,
  PutObjectInputBuffer,
  PutObjectInputStream,
  ScopedDeleteObjectInput,
  ScopedGetObjectInput,
  ScopedPutObjectInput,
} from "./types.js";

describe("PutObjectInput discriminated union", () => {
  it("accepts buffer variant", () => {
    const input: PutObjectInput = {
      ownerId: "tea-123",
      region: "frankfurt",
      key: "test.txt",
      data: Buffer.from("hello"),
    };
    expectTypeOf(input).toMatchTypeOf<PutObjectInput>();
  });

  it("accepts stream variant with required size", () => {
    const input: PutObjectInput = {
      ownerId: "tea-123",
      region: "frankfurt",
      key: "test.txt",
      data: {} as Readable,
      size: 100,
    };
    expectTypeOf(input).toMatchTypeOf<PutObjectInput>();
  });

  it("union includes both variants", () => {
    expectTypeOf<PutObjectInput>().toMatchTypeOf<PutObjectInputBuffer | PutObjectInputStream>();
  });
});

describe("ObjectIdentifier type", () => {
  it("requires tea- prefix on ownerId", () => {
    expectTypeOf<ObjectIdentifier["ownerId"]>().toEqualTypeOf<`tea-${string}`>();
  });

  it("has required key property", () => {
    expectTypeOf<ObjectIdentifier>().toHaveProperty("key");
    expectTypeOf<ObjectIdentifier["key"]>().toEqualTypeOf<string>();
  });
});

describe("Scoped types omit ObjectScope fields", () => {
  it("ScopedPutObjectInput omits ownerId and region", () => {
    expectTypeOf<ScopedPutObjectInput>().not.toHaveProperty("ownerId");
    expectTypeOf<ScopedPutObjectInput>().not.toHaveProperty("region");
    expectTypeOf<ScopedPutObjectInput>().toHaveProperty("key");
    expectTypeOf<ScopedPutObjectInput>().toHaveProperty("data");
  });

  it("ScopedGetObjectInput omits ownerId and region", () => {
    expectTypeOf<ScopedGetObjectInput>().not.toHaveProperty("ownerId");
    expectTypeOf<ScopedGetObjectInput>().not.toHaveProperty("region");
    expectTypeOf<ScopedGetObjectInput>().toHaveProperty("key");
  });

  it("ScopedDeleteObjectInput omits ownerId and region", () => {
    expectTypeOf<ScopedDeleteObjectInput>().not.toHaveProperty("ownerId");
    expectTypeOf<ScopedDeleteObjectInput>().not.toHaveProperty("region");
    expectTypeOf<ScopedDeleteObjectInput>().toHaveProperty("key");
  });

  it("ObjectScope has ownerId and region", () => {
    expectTypeOf<ObjectScope>().toHaveProperty("ownerId");
    expectTypeOf<ObjectScope>().toHaveProperty("region");
  });
});

describe("GetObjectInput and DeleteObjectInput extend ObjectIdentifier", () => {
  it("GetObjectInput matches ObjectIdentifier", () => {
    expectTypeOf<GetObjectInput>().toMatchTypeOf<ObjectIdentifier>();
  });

  it("DeleteObjectInput matches ObjectIdentifier", () => {
    expectTypeOf<DeleteObjectInput>().toMatchTypeOf<ObjectIdentifier>();
  });
});
