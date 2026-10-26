import type { components } from "../../generated/schema.js";

/**
 * The plans the API offered when this SDK was released, for editor hints. The API can add plans
 * at any time, and `create()` sends any plan string as is, so a newer plan works without an SDK
 * update.
 */
export type SandboxPlan = Exclude<
  components["schemas"]["sandboxPlan"],
  "starter" | "standard" | "pro"
>;
