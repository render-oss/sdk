import type { components } from "./schema.js";

/**
 * Execution context passed to every task as its first argument.
 *
 * The context is how a task reaches the rest of the workflow system.
 */
export interface TaskContext {
  /** Metadata about this task's execution. */
  readonly metadata: TaskRunMetadata;

  /**
   * Run another task on its own compute and wait for its result.
   */
  run<TArgs extends unknown[], TResult>(
    task: TaskDefinition<TArgs, TResult>,
    ...args: TArgs
  ): Promise<TResult>;
}

/**
 * The function body of a task.
 */
export type TaskFunction<TArgs extends unknown[] = unknown[], TResult = unknown> = (
  ctx: TaskContext,
  ...args: TArgs
) => TResult | Promise<TResult>;

/**
 * A task function with its argument and result types erased.
 *
 * Used where tasks of differing signatures are stored together, such as the
 * registry. The parameters are `any[]` rather than `unknown[]` because
 * parameter positions are checked contravariantly: a
 * `TaskFunction<[number], string>` is not assignable to
 * `TaskFunction<unknown[], unknown>`, so the stricter type would force a cast at
 * every registration site.
 */
export type AnyTaskFunction = TaskFunction<any[], any>;

/**
 * A registered task.
 *
 * Pass it to {@link TaskContext.run}.
 */
export interface TaskDefinition<TArgs extends unknown[] = unknown[], TResult = unknown> {
  /** Name the task is registered under. */
  readonly name: string;
  /**
   * The undecorated function body.
   *
   * Invoke it directly to run the task in-process against a context you
   * supply, which is how tasks are exercised in unit tests.
   */
  readonly func: TaskFunction<TArgs, TResult>;
}

export type TaskOptions = components["schemas"]["TaskOptions"];

/** Metadata about the task execution. */
export interface TaskRunMetadata {
  /** This run's ID. */
  readonly taskRunId?: string;
  /** The root run's ID. An empty root ID is undefined. */
  readonly rootTaskRunId?: string;
  /** The parent run's ID. Undefined for root runs. */
  readonly parentTaskRunId?: string;
}

/**
 * Task metadata
 */
export interface TaskMetadata {
  name: string;
  func: AnyTaskFunction;
  options?: TaskOptions;
}

/**
 * Workflow metadata
 */
export interface FlowMetadata {
  name: string;
  func: AnyFlowFunction;
  options?: TaskOptions;
}

/**
 * Task input from the workflow system
 */
export interface TaskInput {
  task_name: string;
  input: any[];
}

/**
 * Task callback request/response types
 */

export type CallbackRequest = components["schemas"]["CallbackRequest"];

export type GetInputResponse = components["schemas"]["InputResponse"];

export type RunSubtaskRequest = components["schemas"]["RunSubtaskRequest"];

export type RunSubtaskResponse = components["schemas"]["RunSubtaskResponse"];

export type GetSubtaskResultRequest = components["schemas"]["SubtaskResultRequest"];

export type GetSubtaskResultResponse = components["schemas"]["SubtaskResultResponse"];

export type RegisterTasksRequest = components["schemas"]["Tasks"];

export type TaskErrorBody = components["schemas"]["TaskError"];

export type StepKey = components["schemas"]["StepKey"];

export type StepRecord = components["schemas"]["StepRecord"];

export type StepAttemptRecord = components["schemas"]["StepAttemptRecord"];

export type WireStepError = components["schemas"]["StepError"];

export type StepStartRequest = components["schemas"]["StepStartRequest"];

export type StepStartResponse = components["schemas"]["StepStartResponse"];

export type StepAttemptRequest = components["schemas"]["StepAttemptRequest"];

export type StepAttemptResponse = components["schemas"]["StepAttemptResponse"];

export type StepCompleteRequest = Omit<components["schemas"]["StepCompleteRequest"], "outcome"> & {
  outcome: StepOutcome;
};

/**
 * A step's result: a success, with or without an output, or the failed attempt
 * that ends it. Mirrors the step-history proto's oneof, which the generated
 * schema can only express as two optional fields.
 */
export type StepOutcome = Omit<components["schemas"]["StepOutcome"], "output" | "final_attempt"> &
  (
    | { output?: Payload; final_attempt?: never }
    | { output?: never; final_attempt: components["schemas"]["StepAttempt"] }
  );

export type Payload = components["schemas"]["Payload"];

export type StepCompleteResponse = components["schemas"]["StepCompleteResponse"];

export type WaitRequest = components["schemas"]["WaitRequest"];

export type WaitResponse = components["schemas"]["WaitResponse"];

export type DeterminismDetails = components["schemas"]["DeterminismDetails"];

/**
 * Retry configuration for task execution
 */
export interface Retry {
  maxRetries: number;
  waitDurationMs: number;
  backoffScaling?: number; // default 1.5
}

/**
 * Task execution options
 */
export interface RegisterTaskOptions {
  retry?: Retry;
  timeoutSeconds?: number;
  /**
   * Resource plan for task execution.
   * Common plans include:
   * - "starter": 0.5 CPU, 512MB memory
   * - "standard": 1 CPU, 2GB memory (default)
   * - "pro": 2 CPU, 4GB memory
   */
  plan?: string;
  name: string;
}

/**
 * Workflow options. A workflow takes no retry policy: it recovers from
 * infrastructure failures and replays instead.
 */
export interface FlowOptions {
  name: string;
  timeoutSeconds?: number;
  /** Resource plan for each workflow attempt. See {@link RegisterTaskOptions.plan}. */
  plan?: string;
  /** Not allowed on a workflow. */
  retry?: never;
}

/** Metadata about a workflow run. */
export interface FlowRunMetadata {
  readonly flowRunId: string;
}

/** Options for a step. */
export interface StepOptions {
  /** Retries in-process. Defaults to a single attempt. */
  retry?: Retry;
}

/**
 * The context passed to a workflow as its first argument.
 *
 * Every call on it is a durable step. A step's result is recorded once it
 * finishes, and when the workflow replays after a crash or a wait,
 * finished steps return their recorded result instead of running again.
 *
 * Workflow code must be deterministic: it has to make the same `ctx` calls in
 * the same order with the same inputs on every replay. Put anything
 * non-deterministic, such as I/O, clocks or random values, inside a step.
 * Steps run one at a time; `Promise.all` over `ctx` calls is not currently supported.
 */
export interface FlowContext {
  /** Metadata about this workflow run. */
  readonly metadata: FlowRunMetadata;

  /**
   * Invoke a registered task detached: its own task run, on its own
   * compute, under its own retry policy. The workflow waits for its result.
   *
   * Not supported yet: throws a `RenderError`. Use `step` instead.
   */
  invoke<TArgs extends unknown[], TResult>(
    task: TaskDefinition<TArgs, TResult>,
    ...args: TArgs extends [] ? [args?: TArgs] : [args: TArgs]
  ): Promise<Awaited<TResult>>;

  /**
   * Run a plain function as an inline step, inside this process. The function
   * gets no context and can't make `ctx` calls. `name` is the step's name in
   * history and the dashboard.
   */
  step<TArgs extends unknown[], TResult>(
    name: string,
    fn: (...args: TArgs) => TResult,
    args: TArgs,
    options?: StepOptions,
  ): Promise<Awaited<TResult>>;

  /**
   * Run a zero-argument function as an inline step. `name` is the step's name
   * in history and the dashboard.
   */
  step<TResult>(name: string, fn: () => TResult, options?: StepOptions): Promise<Awaited<TResult>>;
}

/**
 * The function body of a workflow.
 */
export type FlowFunction<TArgs extends unknown[] = unknown[], TResult = unknown> = (
  ctx: FlowContext,
  ...args: TArgs
) => TResult | Promise<TResult>;

/** A workflow function with its argument and result types erased. */
export type AnyFlowFunction = FlowFunction<any[], any>;

/**
 * A registered workflow.
 */
export interface FlowDefinition<TArgs extends unknown[] = unknown[], TResult = unknown> {
  /** Name the workflow is registered under. */
  readonly name: string;
  /** The undecorated function body. */
  readonly func: FlowFunction<TArgs, TResult>;
  readonly flow: true;
}
