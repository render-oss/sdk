import type { Readable } from "node:stream";
import type {
  BlobIdentifier,
  BlobScope,
  DeleteBlobInput,
  GetBlobInput,
  PutBlobInput,
  PutBlobInputBuffer,
  PutBlobInputStream,
  ScopedDeleteBlobInput,
  ScopedGetBlobInput,
  ScopedPutBlobInput,
} from "./types.js";

describe("PutBlobInput discriminated union", () => {
  it("accepts buffer variant", () => {
    const input: PutBlobInput = {
      ownerId: "tea-123",
      region: "frankfurt",
      key: "test.txt",
      data: Buffer.from("hello"),
    };
    expectTypeOf(input).toMatchTypeOf<PutBlobInput>();
  });

  it("accepts stream variant with required size", () => {
    const input: PutBlobInput = {
      ownerId: "tea-123",
      region: "frankfurt",
      key: "test.txt",
      data: {} as Readable,
      size: 100,
    };
    expectTypeOf(input).toMatchTypeOf<PutBlobInput>();
  });

  it("union includes both variants", () => {
    expectTypeOf<PutBlobInput>().toMatchTypeOf<PutBlobInputBuffer | PutBlobInputStream>();
  });
});

describe("BlobIdentifier type", () => {
  it("requires tea- prefix on ownerId", () => {
    expectTypeOf<BlobIdentifier["ownerId"]>().toEqualTypeOf<`tea-${string}`>();
  });

  it("has required key property", () => {
    expectTypeOf<BlobIdentifier>().toHaveProperty("key");
    expectTypeOf<BlobIdentifier["key"]>().toEqualTypeOf<string>();
  });
});

describe("Scoped types omit BlobScope fields", () => {
  it("ScopedPutBlobInput omits ownerId and region", () => {
    expectTypeOf<ScopedPutBlobInput>().not.toHaveProperty("ownerId");
    expectTypeOf<ScopedPutBlobInput>().not.toHaveProperty("region");
    expectTypeOf<ScopedPutBlobInput>().toHaveProperty("key");
    expectTypeOf<ScopedPutBlobInput>().toHaveProperty("data");
  });

  it("ScopedGetBlobInput omits ownerId and region", () => {
    expectTypeOf<ScopedGetBlobInput>().not.toHaveProperty("ownerId");
    expectTypeOf<ScopedGetBlobInput>().not.toHaveProperty("region");
    expectTypeOf<ScopedGetBlobInput>().toHaveProperty("key");
  });

  it("ScopedDeleteBlobInput omits ownerId and region", () => {
    expectTypeOf<ScopedDeleteBlobInput>().not.toHaveProperty("ownerId");
    expectTypeOf<ScopedDeleteBlobInput>().not.toHaveProperty("region");
    expectTypeOf<ScopedDeleteBlobInput>().toHaveProperty("key");
  });

  it("BlobScope has ownerId and region", () => {
    expectTypeOf<BlobScope>().toHaveProperty("ownerId");
    expectTypeOf<BlobScope>().toHaveProperty("region");
  });
});

describe("GetBlobInput and DeleteBlobInput extend BlobIdentifier", () => {
  it("GetBlobInput matches BlobIdentifier", () => {
    expectTypeOf<GetBlobInput>().toMatchTypeOf<BlobIdentifier>();
  });

  it("DeleteBlobInput matches BlobIdentifier", () => {
    expectTypeOf<DeleteBlobInput>().toMatchTypeOf<BlobIdentifier>();
  });
});
