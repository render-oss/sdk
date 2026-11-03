import { TaskRegistry } from "./registry.js";
import { registerAndScheduleStart } from "./task.js";
import type { FlowDefinition, FlowFunction, FlowOptions } from "./types.js";

/**
 * Register a durable workflow.
 *
 * A workflow takes a {@link FlowContext} as its first parameter, followed
 * by its inputs. Each `ctx` call is a durable step: `ctx.step(name, fn, [args])`
 * runs a plain function inline.
 *
 * After a crash, a later attempt reruns the workflow from the top, and `ctx`
 * calls for finished steps return their recorded results. Workflow code must
 * therefore be deterministic.
 *
 * Workflows don't take a retry policy: they recover from infrastructure
 * failures and replay instead.
 *
 * @param options Workflow options, including the name it registers under
 * @param func Workflow function, taking a FlowContext as its first parameter
 * @returns A workflow definition
 */
export function flow<TArgs extends unknown[], TResult>(
  options: FlowOptions,
  func: FlowFunction<TArgs, TResult>,
): FlowDefinition<TArgs, TResult> {
  registerAndScheduleStart("Workflow", options.name, () =>
    TaskRegistry.getInstance().registerFlow(func, options),
  );

  return Object.freeze({
    name: options.name,
    func,
    flow: true as const,
  });
}
