import { RenderError } from "../../errors.js";
import type { DeterminismDetails, TaskErrorBody, WireStepError } from "../types.js";

/**
 * A step that failed: an inline step that used up its retries, or a detached
 * task whose run failed. A replay rethrows the same error, so catching it
 * is safe in workflow code.
 */
export class StepError extends Error {
  /** The `name` of the error the step threw, such as `"TypeError"`. */
  readonly errorName: string;
  /** Extra fields the original error carried, if any. */
  readonly data?: unknown;

  constructor(error: WireStepError) {
    super(error.message);
    this.name = "StepError";
    this.errorName = error.name;
    if (error.stack) {
      this.stack = error.stack;
    }
    if (error.data) {
      try {
        this.data = JSON.parse(error.data);
      } catch {
        this.data = error.data;
      }
    }
    Object.setPrototypeOf(this, StepError.prototype);
  }

  /** Build the recorded form of anything a step threw. */
  static serialize(error: unknown): WireStepError {
    if (!(error instanceof Error)) {
      return { name: "Error", message: String(error) };
    }

    const wire: WireStepError = { name: error.name, message: error.message };
    if (error.stack) {
      wire.stack = error.stack;
    }
    const extra = Object.fromEntries(Object.entries(error));
    if (Object.keys(extra).length > 0) {
      try {
        wire.data = JSON.stringify(extra);
      } catch {
        // Fields that don't serialize are dropped.
      }
    }
    return wire;
  }

  /** A detached task's failure, as reported for its run. */
  static fromTaskError(error: TaskErrorBody): StepError {
    return new StepError({ name: "TaskError", message: error.details, stack: error.stack_trace });
  }
}

/**
 * A replay made a different `ctx` call than the one recorded in history.
 * It fails the run and can't be caught: later `ctx` calls rethrow it.
 */
export class DeterminismError extends RenderError {
  constructor(readonly details: DeterminismDetails) {
    super(
      `Workflow replay diverged from its history at step ${details.step_key.seq}: ` +
        `${describeKind(details.kind)}. ` +
        `History recorded ${details.expected}; this attempt called ${details.actual}. ` +
        "A workflow must make the same ctx calls in the same order with the same inputs " +
        "on every replay; move non-deterministic work into a step.",
    );
    this.name = "DeterminismError";
    Object.setPrototypeOf(this, DeterminismError.prototype);
  }
}

function describeKind(kind: DeterminismDetails["kind"]): string {
  switch (kind) {
    case "type":
      return "the step type changed";
    case "unknown_type":
      return "the recorded step type is unknown";
    default:
      return "the step's name or input changed";
  }
}

/**
 * The run can't continue, for a reason a replay would hit again, such as a
 * workflow limit. It fails the run and can't be caught.
 */
export class FlowFailedError extends RenderError {
  constructor(message: string) {
    super(message);
    this.name = "FlowFailedError";
    Object.setPrototypeOf(this, FlowFailedError.prototype);
  }
}

/**
 * A step write over a workflow limit. `reason` names the limit; `limit` and
 * `value` are set when the workflow system sent them.
 */
export class WorkflowLimitError extends FlowFailedError {
  constructor(
    message: string,
    readonly reason: TaskErrorBody["reason"],
    readonly limit?: number,
    readonly value?: number,
  ) {
    super(message);
    this.name = "WorkflowLimitError";
    Object.setPrototypeOf(this, WorkflowLimitError.prototype);
  }
}
