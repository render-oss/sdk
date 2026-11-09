/**
 * The task wire encoding: an input is the base64 of a JSON array of
 * arguments, and an output is the base64 of a JSON one-element array holding
 * the result. Tasks, subtasks and workflow steps all use it; an invoked
 * step records its child's input and output objects as they are, so inline
 * steps match them.
 */

export function encodeArgs(args: unknown[]): string {
  return Buffer.from(JSON.stringify(args)).toString("base64");
}

export function decodeArgs(input: string | undefined): unknown {
  if (!input) {
    return undefined;
  }
  return JSON.parse(Buffer.from(input, "base64").toString());
}

/**
 * With strict, throws for values JSON would silently change, such as NaN, a
 * Date or a class instance, as the Python SDK does for steps.
 */
export function encodeOutput(value: unknown, { strict = false } = {}): string {
  if (value === undefined) {
    return "";
  }
  return Buffer.from(JSON.stringify([value], strict ? rejectLossy : undefined)).toString("base64");
}

function rejectLossy(this: unknown, key: string, value: unknown): unknown {
  const original = (this as Record<string, unknown>)[key];
  if (typeof original === "function" || typeof original === "symbol") {
    throw new TypeError(`${typeof original} is not valid JSON`);
  }
  if (original === undefined && Array.isArray(this)) {
    throw new TypeError("undefined in an array is not valid JSON");
  }
  if (typeof original === "number" && !Number.isFinite(original)) {
    throw new TypeError(`${original} is not valid JSON`);
  }
  if (typeof original === "object" && original !== null && !Array.isArray(original)) {
    const proto = Object.getPrototypeOf(original);
    // A plain object's prototype is Object.prototype, from any realm.
    if (proto !== null && Object.getPrototypeOf(proto) !== null) {
      throw new TypeError(`${original.constructor?.name ?? "This object"} is not valid JSON`);
    }
  }
  return value;
}

export function decodeOutput(output: string | undefined): unknown {
  if (!output) {
    return undefined;
  }
  return JSON.parse(Buffer.from(output, "base64").toString())[0];
}

/**
 * JSON with object keys sorted at every level, so two values that encode
 * the same data compare equal whatever order their keys were set in.
 */
export function canonicalJson(value: unknown): string {
  return JSON.stringify(sortKeys(JSON.parse(JSON.stringify(value) ?? "null")));
}

function sortKeys(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(sortKeys);
  }
  if (value !== null && typeof value === "object") {
    const sorted: Record<string, unknown> = {};
    for (const key of Object.keys(value).sort()) {
      sorted[key] = sortKeys((value as Record<string, unknown>)[key]);
    }
    return sorted;
  }
  return value;
}
