import { decodeArgs, decodeOutput, encodeArgs, encodeOutput } from "./encoding.js";

describe("non-strict encoding", () => {
  it.each([
    ["a function", () => 1, null],
    ["a symbol", Symbol("value"), null],
    ["undefined array entries", [undefined, 1], [null, 1]],
    ["omitted properties", { cb: () => 1, value: Symbol("value"), skip: undefined }, {}],
  ])("preserves JSON conversion of %s", (_, value, expected) => {
    expect(decodeOutput(encodeOutput(value))).toEqual(expected);
    expect(decodeOutput(encodeOutput(value, { strict: false }))).toEqual(expected);
    expect(decodeArgs(encodeArgs([value]))).toEqual([expected]);
  });
});
