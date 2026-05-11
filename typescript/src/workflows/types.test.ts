// biome-ignore-all lint/correctness/noUnusedVariables: type-only tests; symbols are referenced for type checking
import type { Readable } from "node:stream";
import {
  type DeleteObjectInput,
  type GetObjectInput,
  ObjectApi,
  type ObjectClient,
  type ObjectData,
  type ObjectIdentifier,
  type ObjectScope,
  type PresignedDownloadUrl,
  type PresignedUploadUrl,
  type PutObjectInput,
  type PutObjectInputBuffer,
  type PutObjectInputStream,
  type PutObjectResult,
  type Region,
  type ScopedDeleteObjectInput,
  type ScopedGetObjectInput,
  type ScopedObjectClient,
  type ScopedPutObjectInput,
} from "../experimental/index.js";
import type { ExperimentalClient } from "../index.js";
import {
  AbortError,
  ClientError,
  getUserAgent,
  Render,
  RenderError,
  ServerError,
  TaskRunError,
  TimeoutError,
  VERSION,
} from "../index.js";
import {
  type CallbackRequest,
  type ClientOptions,
  createWorkflowsClient,
  type GetInputResponse,
  type GetSubtaskResultRequest,
  type GetSubtaskResultResponse,
  getCurrentContext,
  type ListTaskRunsParams,
  type RegisterTaskOptions,
  type RegisterTasksRequest,
  type Retry,
  type RunSubtaskRequest,
  type RunSubtaskResponse,
  type RunTaskRequest,
  run,
  setCurrentContext,
  startTaskServer,
  type TaskContext,
  type TaskData,
  TaskEventType,
  TaskExecutor,
  type TaskFunction,
  type TaskInput,
  type TaskMetadata,
  type TaskOptions,
  TaskRegistry,
  type TaskResult,
  type TaskRun,
  type TaskRunDetails,
  TaskRunResult,
  TaskRunStatus,
  type TaskRunWithCursor,
  type TaskSlug,
  task,
  type WorkflowsClient,
} from "./index.js";

describe("Exported symbols", () => {
  it("ObjectApi is a constructor", () => {
    expect(typeof ObjectApi).toBe("function");
  });

  it("createWorkflowsClient returns WorkflowsClient", () => {
    expectTypeOf(createWorkflowsClient).toBeFunction();
    expectTypeOf(createWorkflowsClient).parameter(0).toExtend<ClientOptions | undefined>();
    expectTypeOf(createWorkflowsClient).returns.toExtend<WorkflowsClient>();
  });

  it("run is an async function accepting socket path", () => {
    expectTypeOf(run).toBeFunction();
    expectTypeOf(run).parameter(0).toEqualTypeOf<string>();
    expectTypeOf(run).returns.toExtend<Promise<void>>();
  });

  it("startTaskServer is an async function", () => {
    expectTypeOf(startTaskServer).toBeFunction();
    expectTypeOf(startTaskServer).returns.toExtend<Promise<void>>();
  });

  it("TaskExecutor is a constructor", () => {
    expect(typeof TaskExecutor).toBe("function");
    expectTypeOf<InstanceType<typeof TaskExecutor>>().toHaveProperty("executeTask");
  });

  it("TaskRunResult is a constructor with taskRunId and get()", () => {
    expect(typeof TaskRunResult).toBe("function");
    expectTypeOf<InstanceType<typeof TaskRunResult>>().toHaveProperty("get");
    expectTypeOf<InstanceType<typeof TaskRunResult>>().toHaveProperty("taskRunId");
  });

  it("TaskEventType maps to SSE event name strings", () => {
    expect(TaskEventType.COMPLETED).toBe("task.completed");
    expect(TaskEventType.SUCCEEDED).toBe("task.succeeded");
    expect(TaskEventType.FAILED).toBe("task.failed");
    expect(TaskEventType.CANCELED).toBe("task.canceled");
  });

  it("WorkflowsClient exposes startTask and streaming helpers", () => {
    expectTypeOf<WorkflowsClient["startTask"]>().returns.toExtend<Promise<TaskRunResult>>();
    expectTypeOf<WorkflowsClient["cancelTaskRun"]>().parameter(0).toEqualTypeOf<string>();
    expectTypeOf<WorkflowsClient["taskRunEvents"]>().parameter(0).toEqualTypeOf<string[]>();
  });
});

describe("TaskFunction type", () => {
  it("accepts typed args and returns typed result", () => {
    expectTypeOf<TaskFunction<[string, number], boolean>>().toExtend<
      (a: string, b: number) => boolean | Promise<boolean>
    >();
  });

  it("defaults to any[] args and any result", () => {
    expectTypeOf<TaskFunction>().toExtend<(...args: any[]) => any>();
  });

  it("allows async return type", () => {
    const asyncFn: TaskFunction<[string], number> = async (s) => s.length;
    expectTypeOf(asyncFn).returns.toExtend<number | Promise<number>>();
  });

  it("allows sync return type", () => {
    const syncFn: TaskFunction<[string], number> = (s) => s.length;
    expectTypeOf(syncFn).returns.toExtend<number | Promise<number>>();
  });
});

describe("TaskResult type", () => {
  it("get() returns Promise<T>", () => {
    expectTypeOf<TaskResult<string>>().toHaveProperty("get");
    expectTypeOf<TaskResult<string>["get"]>().returns.toEqualTypeOf<Promise<string>>();
  });

  it("preserves generic parameter", () => {
    type NumberResult = TaskResult<number>;
    type StringResult = TaskResult<string>;
    expectTypeOf<NumberResult["get"]>().returns.toEqualTypeOf<Promise<number>>();
    expectTypeOf<StringResult["get"]>().returns.toEqualTypeOf<Promise<string>>();
  });
});

describe("TaskContext type", () => {
  it("has executeTask method", () => {
    expectTypeOf<TaskContext>().toHaveProperty("executeTask");
  });

  it("executeTask is callable", () => {
    type ExecuteTask = TaskContext["executeTask"];
    expectTypeOf<ExecuteTask>().toBeCallableWith(
      {} as TaskFunction<[string], number>,
      "taskName",
      "arg",
    );
  });
});

async function testRenderClient() {
  const render = new Render({
    baseUrl: "https://api.render.com",
    token: "test-token",
    useLocalDev: false,
    localDevUrl: "http://localhost:8080",
  });

  const renderDefault = new Render();

  const workflows: WorkflowsClient = render.workflows;
  const experimental: ExperimentalClient = render.experimental;
  const objects: ObjectClient = render.experimental.storage.objects;
}

async function testWorkflowsClient() {
  const render = new Render({ token: "test" });

  const taskResult: TaskRunDetails = await render.workflows.runTask("workflow-slug/task-name", [
    "arg1",
    "arg2",
    { key: "value" },
  ]);

  const id: string = taskResult.id;
  const taskId: string = taskResult.taskId;
  const status: TaskRunDetails["status"] = taskResult.status;
  const results: unknown = taskResult.results;
  const error: string | undefined = taskResult.error;
  const startedAt: string | undefined = taskResult.startedAt;
  const completedAt: string | undefined = taskResult.completedAt;
  const input: unknown[] | { [key: string]: unknown } = taskResult.input;
  const parentTaskRunId: string = taskResult.parentTaskRunId;
  const rootTaskRunId: string = taskResult.rootTaskRunId;
  const retries: number = taskResult.retries;

  const controller = new AbortController();
  const taskResultWithSignal: TaskRunDetails = await render.workflows.runTask(
    "my-workflow/greet",
    ["World"],
    controller.signal,
  );

  const taskRunDetails: TaskRunDetails = await render.workflows.getTaskRun("task-run-id-123");

  const taskRuns: TaskRunWithCursor[] = await render.workflows.listTaskRuns({
    cursor: "cursor-123",
    limit: 50,
    taskSlug: ["tsk-1234", "my-workflow/my-task"],
    rootTaskRunId: ["root-task-run-id"],
    ownerId: ["owner-123"],
    workflowVersionId: ["version-123"],
    workflowId: ["workflow-123"],
  });

  if (taskRuns.length > 0) {
    const run = taskRuns[0].taskRun;
    const runId: string = run.id;
    const runTaskId: string = run.taskId;
    const runStatus: TaskRun["status"] = run.status;
    const runStartedAt: string | undefined = run.startedAt;
    const runCompletedAt: string | undefined = run.completedAt;
    const runParentTaskRunId: string = run.parentTaskRunId;
    const runRootTaskRunId: string = run.rootTaskRunId;
    const runRetries: number = run.retries;
  }
}

function testTaskRunStatus() {
  const pending: TaskRunStatus = TaskRunStatus.PENDING;
  const running: TaskRunStatus = TaskRunStatus.RUNNING;
  const completed: TaskRunStatus = TaskRunStatus.COMPLETED;
  const succeeded: TaskRunStatus = TaskRunStatus.SUCCEEDED;
  const failed: TaskRunStatus = TaskRunStatus.FAILED;

  const pendingValue: "pending" = TaskRunStatus.PENDING;
  const runningValue: "running" = TaskRunStatus.RUNNING;
  const completedValue: "completed" = TaskRunStatus.COMPLETED;
  const succeededValue: "succeeded" = TaskRunStatus.SUCCEEDED;
  const failedValue: "failed" = TaskRunStatus.FAILED;
}

function testTaskRegistration() {
  const greet = task({ name: "greet" }, (name: string): string => `Hello, ${name}!`);

  const greeting = greet("World");

  const asyncGreet = task(
    { name: "asyncGreet" },
    async (name: string): Promise<string> => `Hello, ${name}!`,
  );

  const retryTask = task(
    {
      name: "retryTask",
      retry: {
        maxRetries: 3,
        waitDurationMs: 1000,
        backoffScaling: 2.0,
      },
    },
    async (data: number[]): Promise<number> => data.reduce((a, b) => a + b, 0),
  );

  const timeoutTask = task(
    {
      name: "timeoutTask",
      timeoutSeconds: 60,
    },
    async (): Promise<void> => {},
  );

  const proTask = task(
    {
      name: "proTask",
      plan: "pro",
    },
    async (input: { x: number; y: number }): Promise<number> => input.x + input.y,
  );

  const fullOptionsTask = task(
    {
      name: "fullOptionsTask",
      retry: {
        maxRetries: 5,
        waitDurationMs: 500,
        backoffScaling: 1.5,
      },
      timeoutSeconds: 120,
      plan: "standard",
    },
    async <T>(items: T[]): Promise<T[]> => items.reverse(),
  );
}

async function testTaskContext() {
  const context: TaskContext | undefined = getCurrentContext();

  if (context) {
    const mockTask = async (x: number, y: number): Promise<number> => x + y;
    const result: TaskResult<number> = context.executeTask(mockTask, "add", 1, 2);

    const value: number = await result.get();
  }

  const mockContext: TaskContext = {
    executeTask: <TArgs extends any[], TResult>(
      taskFn: TaskFunction<TArgs, TResult>,
      _taskName: string,
      ...args: TArgs
    ): TaskResult<TResult> => ({
      get: async () => taskFn(...args),
    }),
  };

  const contextResult: string = await setCurrentContext(mockContext, async () => {
    return "result from context";
  });
}

function testTaskRegistry() {
  const registry = TaskRegistry.getInstance();

  const myTask: TaskFunction<[string], string> = (name: string) => `Hello, ${name}`;
  registry.register(myTask, { name: "myTask" });

  const metadata: TaskMetadata | undefined = registry.get("myTask");
  if (metadata) {
    const name: string = metadata.name;
    const func: TaskFunction = metadata.func;
    const options: TaskOptions | undefined = metadata.options;
  }

  const hasTask: boolean = registry.has("myTask");
  const taskNames: string[] = registry.getAllTaskNames();
  const allTasks: TaskMetadata[] = registry.getAllTasks();
  registry.clear();
}

function testTaskTypes() {
  const syncTask: TaskFunction<[number, number], number> = (a, b) => a + b;
  const asyncTask: TaskFunction<[string], Promise<string>> = async (s) => s.toUpperCase();

  const taskInput: TaskInput = {
    task_name: "myTask",
    input: [1, 2, 3],
  };

  const retry: Retry = {
    maxRetries: 3,
    waitDurationMs: 1000,
    backoffScaling: 1.5,
  };

  const options: RegisterTaskOptions = {
    name: "testTask",
    retry: {
      maxRetries: 3,
      waitDurationMs: 1000,
    },
    timeoutSeconds: 60,
    plan: "starter",
  };

  const runTaskRequest: RunTaskRequest = {
    task: "workflow-slug/task-name",
    input: ["arg1", "arg2"],
  };

  const taskSlug: TaskSlug = "my-workflow/my-task";
  const taskData: TaskData = ["arg1", 42, { nested: true }];

  type CallbackRequestCheck = CallbackRequest;
  type GetInputResponseCheck = GetInputResponse;
  type RunSubtaskRequestCheck = RunSubtaskRequest;
  type RunSubtaskResponseCheck = RunSubtaskResponse;
  type GetSubtaskResultRequestCheck = GetSubtaskResultRequest;
  type GetSubtaskResultResponseCheck = GetSubtaskResultResponse;
  type RegisterTasksRequestCheck = RegisterTasksRequest;
}

function testErrorTypes() {
  const renderError = new RenderError("Something went wrong");
  const renderErrorMsg: string = renderError.message;
  const renderErrorName: string = renderError.name;

  const taskRunError = new TaskRunError("Task failed", "task-run-123", "Division by zero");
  const taskRunErrorMsg: string = taskRunError.message;
  const taskRunErrorId: string | undefined = taskRunError.taskRunId;
  const taskRunErrorDetail: string | undefined = taskRunError.taskError;

  const clientError = new ClientError("Not found", 404, { detail: "Resource not found" });
  const clientErrorMsg: string = clientError.message;
  const clientErrorCode: number = clientError.statusCode;
  const clientErrorResponse: any = clientError.response;

  const serverError = new ServerError("Internal error", 500, { detail: "Database unavailable" });
  const serverErrorMsg: string = serverError.message;
  const serverErrorCode: number = serverError.statusCode;
  const serverErrorResponse: any = serverError.response;

  const timeoutError = new TimeoutError("Request timed out after 30s");
  const timeoutErrorMsg: string = timeoutError.message;

  const abortError = new AbortError();
  const abortErrorMsg: string = abortError.message;
  const abortErrorName: string = abortError.name;

  const isRenderError: boolean = renderError instanceof RenderError;
  const isError: boolean = renderError instanceof Error;
  const taskRunIsRenderError: boolean = taskRunError instanceof RenderError;
  const clientIsRenderError: boolean = clientError instanceof RenderError;
  const serverIsRenderError: boolean = serverError instanceof RenderError;
  const timeoutIsRenderError: boolean = timeoutError instanceof RenderError;
}

function testVersionUtils() {
  const version: string = VERSION;
  const userAgent: string = getUserAgent();
}

async function testObjectClient() {
  const render = new Render({ token: "test" });
  const objects = render.experimental.storage.objects;

  const putBufferResult: PutObjectResult = await objects.put({
    ownerId: "tea-xxxxx",
    region: "oregon",
    key: "path/to/file.png",
    data: Buffer.from("binary content"),
    contentType: "image/png",
  });

  const etag: string | undefined = putBufferResult.etag;

  await objects.put({
    ownerId: "tea-12345",
    region: "frankfurt",
    key: "data.bin",
    data: new Uint8Array([1, 2, 3, 4]),
  });

  await objects.put({
    ownerId: "tea-abcde",
    region: "ohio",
    key: "text.txt",
    data: "Hello, World!",
    size: 13,
    contentType: "text/plain",
  });

  const mockStream = {} as Readable;
  await objects.put({
    ownerId: "tea-stream",
    region: "singapore",
    key: "large-file.zip",
    data: mockStream,
    size: 1024 * 1024,
  });

  const objectData: ObjectData = await objects.get({
    ownerId: "tea-xxxxx",
    region: "oregon",
    key: "path/to/file.png",
  });

  const data: Buffer = objectData.data;
  const size: number = objectData.size;
  const contentType: string | undefined = objectData.contentType;

  await objects.delete({
    ownerId: "tea-xxxxx",
    region: "virginia",
    key: "old-file.txt",
  });
}

async function testScopedObjectClient() {
  const render = new Render({ token: "test" });

  const scopedObjects: ScopedObjectClient = render.experimental.storage.objects.scoped({
    ownerId: "tea-xxxxx",
    region: "oregon",
  });

  const putResult: PutObjectResult = await scopedObjects.put({
    key: "file.png",
    data: Buffer.from("content"),
    contentType: "image/png",
  });

  const objectData: ObjectData = await scopedObjects.get({
    key: "file.png",
  });

  await scopedObjects.delete({
    key: "file.png",
  });
}

function testObjectTypes() {
  const regions: Region[] = ["frankfurt", "oregon", "ohio", "singapore", "virginia"];

  const identifier: ObjectIdentifier = {
    ownerId: "tea-xxxxx",
    region: "oregon",
    key: "my/file/path.txt",
  };

  const scope: ObjectScope = {
    ownerId: "tea-yyyyy",
    region: "frankfurt",
  };

  const bufferInput: PutObjectInputBuffer = {
    ownerId: "tea-xxxxx",
    region: "oregon",
    key: "file.bin",
    data: Buffer.from([1, 2, 3]),
    size: 3,
    contentType: "application/octet-stream",
  };

  const streamInput: PutObjectInputStream = {
    ownerId: "tea-xxxxx",
    region: "oregon",
    key: "large.bin",
    data: {} as Readable,
    size: 1000,
    contentType: "application/octet-stream",
  };

  const putInput: PutObjectInput = bufferInput;
  const putInputStream: PutObjectInput = streamInput;

  const getInput: GetObjectInput = {
    ownerId: "tea-xxxxx",
    region: "oregon",
    key: "file.bin",
  };

  const deleteInput: DeleteObjectInput = {
    ownerId: "tea-xxxxx",
    region: "oregon",
    key: "file.bin",
  };

  const uploadUrl: PresignedUploadUrl = {
    url: "https://s3.amazonaws.com/bucket/key?signature=xxx",
    expiresAt: new Date(),
    maxSizeBytes: 10 * 1024 * 1024,
  };

  const downloadUrl: PresignedDownloadUrl = {
    url: "https://s3.amazonaws.com/bucket/key?signature=xxx",
    expiresAt: new Date(),
  };

  const objectData: ObjectData = {
    data: Buffer.from("content"),
    size: 7,
    contentType: "text/plain",
  };

  const putResult: PutObjectResult = {
    etag: '"abc123"',
  };

  const scopedPut: ScopedPutObjectInput = {
    key: "file.txt",
    data: Buffer.from("hello"),
  };

  const scopedGet: ScopedGetObjectInput = {
    key: "file.txt",
  };

  const scopedDelete: ScopedDeleteObjectInput = {
    key: "file.txt",
  };
}

function testClientOptions() {
  const fullOptions: ClientOptions = {
    token: "my-api-token",
    baseUrl: "https://custom.api.render.com",
    useLocalDev: true,
    localDevUrl: "http://localhost:8080",
  };

  const minimalOptions: ClientOptions = {};
  const tokenOnly: ClientOptions = {
    token: "my-token",
  };

  const localDevOptions: ClientOptions = {
    useLocalDev: true,
    localDevUrl: "http://localhost:3000",
  };
}

function testListTaskRunsParams() {
  const fullParams: ListTaskRunsParams = {
    cursor: "cursor-abc123",
    limit: 100,
    taskSlug: ["tsk-123", "my-workflow/task-a", "my-workflow/task-b:SHA456"],
    rootTaskRunId: ["root-run-1", "root-run-2"],
    ownerId: ["owner-1"],
    workflowVersionId: ["ver-1", "ver-2"],
    workflowId: ["wf-1"],
  };

  const emptyParams: ListTaskRunsParams = {};
  const paginationParams: ListTaskRunsParams = {
    cursor: "next-page",
    limit: 25,
  };
  const taskFilterParams: ListTaskRunsParams = {
    taskSlug: ["my-workflow/my-task"],
  };
}

function testGenericTaskFunctions() {
  const processArray = task(
    { name: "processArray" },
    <T>(items: T[], transform: (item: T) => T): T[] => items.map(transform),
  );

  const numbers = processArray([1, 2, 3], (n) => n * 2);
  const strings = processArray(["a", "b", "c"], (s) => s.toUpperCase());

  const fetchItems = task({ name: "fetchItems" }, async <T>(_ids: string[]): Promise<T[]> => {
    return [] as T[];
  });

  interface HasId {
    id: string;
  }

  const findById = task(
    { name: "findById" },
    <T extends HasId>(items: T[], id: string): T | undefined => {
      return items.find((item) => item.id === id);
    },
  );
}

async function testAsyncWorkflowPatterns() {
  const render = new Render({ token: "test" });

  const result1 = await render.workflows.runTask("workflow/step1", ["input"]);
  const result2 = await render.workflows.runTask("workflow/step2", [result1.results]);

  const [_resultA, _resultB, _resultC] = await Promise.all([
    render.workflows.runTask("workflow/taskA", ["a"]),
    render.workflows.runTask("workflow/taskB", ["b"]),
    render.workflows.runTask("workflow/taskC", ["c"]),
  ]);

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30_000);

  try {
    const timedResult = await render.workflows.runTask(
      "workflow/long-running",
      ["data"],
      controller.signal,
    );
  } catch (error) {
    if (error instanceof AbortError) {
      console.log("Task was aborted");
    }
  } finally {
    clearTimeout(timeoutId);
  }

  const taskRun = await render.workflows.runTask("workflow/async-task", []);
  let currentStatus = taskRun.status;
  while (currentStatus === "running" || currentStatus === "pending") {
    const details = await render.workflows.getTaskRun(taskRun.id);
    currentStatus = details.status;
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
}

type AssertEqual<T, U> = T extends U ? (U extends T ? true : false) : false;

type TaskRunIdIsString = AssertEqual<TaskRun["id"], string>;
type TaskRunStatusIsEnum = AssertEqual<
  TaskRun["status"],
  "pending" | "running" | "completed" | "succeeded" | "failed" | "canceled" | "paused"
>;
type ObjectRegionType = AssertEqual<
  Region,
  "frankfurt" | "oregon" | "ohio" | "singapore" | "virginia"
>;
type OwnerIdFormat = AssertEqual<ObjectIdentifier["ownerId"], `tea-${string}`>;

type RunTaskReturnsDetails =
  Awaited<ReturnType<WorkflowsClient["runTask"]>> extends TaskRunDetails ? true : never;
type GetTaskRunReturnsDetails =
  Awaited<ReturnType<WorkflowsClient["getTaskRun"]>> extends TaskRunDetails ? true : never;
type ListTaskRunsReturnsArray =
  Awaited<ReturnType<WorkflowsClient["listTaskRuns"]>> extends TaskRunWithCursor[] ? true : never;

type TaskRunErrorExtendsRender = TaskRunError extends RenderError ? true : never;
type ClientErrorExtendsRender = ClientError extends RenderError ? true : never;
type ServerErrorExtendsRender = ServerError extends RenderError ? true : never;
type TimeoutErrorExtendsRender = TimeoutError extends RenderError ? true : never;
type RenderErrorExtendsError = RenderError extends Error ? true : never;
