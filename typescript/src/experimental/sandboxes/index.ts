import type { Readable } from "node:stream";
import type { Client } from "openapi-fetch";

import { AbortError, RenderError } from "../../errors.js";
import type { components, paths } from "../../generated/schema.js";

import { getApiError } from "../../utils/http.js";
import { getUserAgent } from "../../version.js";

const LEADING_SPACE = /^ /;
const TRAILING_CARRIAGE_RETURN = /\r$/;

type SandboxExecOutputEvent = {
  stream: "stdout" | "stderr";
  data: string;
};

type SandboxExecExitEvent = {
  exit_code: number;
};

type SandboxExecErrorEvent = {
  status: number;
  message: string;
};

type SandboxConnectOperation =
  paths["/sandboxes/{sandboxId}/runs/{operation}/token"]["post"]["parameters"]["path"]["operation"];

type SandboxFileOperation =
  paths["/sandboxes/{sandboxId}/files/{operation}/token"]["post"]["parameters"]["path"]["operation"];

export type SandboxUploadData = Buffer | Uint8Array | string | Readable;

export type SandboxUploadContentType =
  | "application/octet-stream"
  | "application/x-tar"
  | "application/gzip";

export type SandboxUploadOptions = {
  contentType?: SandboxUploadContentType;
  signal?: AbortSignal;
};

export type SandboxDownload = {
  data: Buffer;
  size: number;
  contentType?: string;
};

export type SandboxExecEvent =
  | ({ type: "output" } & SandboxExecOutputEvent)
  | ({ type: "exit" } & SandboxExecExitEvent);

/** Options for creating a sandbox. Unset fields fall back to the API's defaults. */
export type SandboxCreateInput = {
  ownerId?: `tea-${string}`;
  plan?: components["schemas"]["sandboxPlan"];
  /** Maximum sandbox lifetime in seconds. The API defaults to 7200. */
  timeoutSeconds?: number;
  /** Defaults to the client's region, then to the workspace default. */
  region?: string;
  networkPolicy?: components["schemas"]["sandboxNetworkPolicy"];
  /** Environment variables injected into the sandbox at creation. */
  env?: Record<string, string>;
};

/** A sandbox group as returned by the API. */
export type SandboxGroup = components["schemas"]["sandboxGroup"];

/** A sandbox group paired with its pagination cursor. */
export type SandboxGroupWithCursor = components["schemas"]["sandboxGroupWithCursor"];

/** Options for listing sandbox groups. */
export type SandboxGroupListInput = {
  /** Defaults to the client's owner ID. */
  ownerId?: `tea-${string}`;
};

export class SandboxExecStreamError extends RenderError {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "SandboxExecStreamError";
    Object.setPrototypeOf(this, SandboxExecStreamError.prototype);
  }
}

export class SandboxesClient {
  private readonly defaultOwnerId?: string;
  private readonly defaultRegion?: string;

  constructor(
    private readonly apiClient: Client<paths>,
    defaultOwnerId?: string,
    defaultRegion?: string,
  ) {
    this.defaultOwnerId = defaultOwnerId;
    this.defaultRegion = defaultRegion;
  }

  private resolveOwnerId(ownerId?: `tea-${string}`): `tea-${string}` {
    const resolved = ownerId || this.defaultOwnerId;
    if (!resolved) {
      throw new RenderError(
        "ownerId is required. Provide it as a parameter or set the RENDER_WORKSPACE_ID environment variable.",
      );
    }
    return resolved as `tea-${string}`;
  }

  async get(sandboxId: string, ownerId?: `tea-${string}`) {
    const { data, error, response } = await this.apiClient.GET("/sandboxes/{sandboxId}", {
      params: {
        path: { sandboxId },
        query: { ownerId: this.resolveOwnerId(ownerId) },
      },
    });
    if (error) {
      throw getTypedApiError(error, response, "Failed to get sandbox");
    }
    return data;
  }

  async create(input: SandboxCreateInput = {}) {
    const region = input.region ?? this.defaultRegion;
    const body = {
      ownerId: this.resolveOwnerId(input.ownerId),
      ...(input.plan ? { plan: input.plan } : {}),
      ...(input.timeoutSeconds === undefined ? {} : { timeoutSeconds: input.timeoutSeconds }),
      ...(region ? { region } : {}),
      ...(input.networkPolicy ? { networkPolicy: input.networkPolicy } : {}),
      ...(input.env ? { env: input.env } : {}),
    } as components["schemas"]["sandboxPOST"];
    const { data, error, response } = await this.apiClient.POST("/sandboxes", { body });
    if (error) {
      throw getTypedApiError(error, response, "Failed to create sandbox");
    }
    return data;
  }

  async list({
    ownerId,
    cursor,
    limit,
    status,
  }: {
    ownerId?: `tea-${string}`;
    cursor?: string;
    limit?: number;
    status?: components["schemas"]["sandboxStatus"][];
  } = {}) {
    const { data, error, response } = await this.apiClient.GET("/sandboxes", {
      params: {
        query: {
          ownerId: this.resolveOwnerId(ownerId),
          cursor,
          limit,
          status,
        },
      },
    });
    if (error) {
      throw getTypedApiError(error, response, "Failed to list sandboxes");
    }
    return data;
  }

  async listGroups({ ownerId }: SandboxGroupListInput = {}): Promise<SandboxGroupWithCursor[]> {
    const { data, error, response } = await this.apiClient.GET("/sandbox-groups", {
      params: {
        query: {
          ownerId: [this.resolveOwnerId(ownerId)],
        },
      },
    });
    if (error) {
      throw getTypedApiError(error, response, "Failed to list sandbox groups");
    }
    return data;
  }

  async terminate(sandboxId: string, ownerId?: `tea-${string}`): Promise<void> {
    const { error, response } = await this.apiClient.POST("/sandboxes/{sandboxId}/terminate", {
      params: {
        path: { sandboxId },
        query: { ownerId: this.resolveOwnerId(ownerId) },
      },
    });
    if (error) {
      throw getTypedApiError(error, response, "Failed to terminate sandbox");
    }
  }

  async upload(
    sandboxId: string,
    path: string,
    data: SandboxUploadData,
    ownerId?: `tea-${string}`,
    options: SandboxUploadOptions = {},
  ): Promise<void> {
    if (options.signal?.aborted) {
      throw new AbortError();
    }

    const tokenResponse = await this.getFileConnectToken(sandboxId, path, "upload", ownerId);
    let response: Response;
    try {
      response = await fetch(tokenResponse.uri, {
        method: tokenResponse.method,
        headers: {
          Authorization: `Bearer ${tokenResponse.token}`,
          "Content-Type": options.contentType ?? "application/octet-stream",
          "User-Agent": getUserAgent(),
        },
        body: data as Buffer | Uint8Array | string,
        duplex: "half",
        signal: options.signal,
      });
      if (!response.ok) {
        throw await getResponseError(response, "Failed to upload sandbox file");
      }
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        throw new AbortError();
      }
      throw err;
    }
  }

  async download(
    sandboxId: string,
    path: string,
    ownerId?: `tea-${string}`,
    signal?: AbortSignal,
  ): Promise<SandboxDownload> {
    if (signal?.aborted) {
      throw new AbortError();
    }

    const tokenResponse = await this.getFileConnectToken(sandboxId, path, "download", ownerId);
    try {
      const response = await fetch(tokenResponse.uri, {
        method: tokenResponse.method,
        headers: {
          Authorization: `Bearer ${tokenResponse.token}`,
          "User-Agent": getUserAgent(),
        },
        signal,
      });

      if (!response.ok) {
        throw await getResponseError(response, "Failed to download sandbox file");
      }

      const data = Buffer.from(await response.arrayBuffer());
      return {
        data,
        size: data.byteLength,
        contentType: response.headers.get("Content-Type") ?? undefined,
      };
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        throw new AbortError();
      }
      throw err;
    }
  }

  private async getRunConnectToken(
    sandboxId: string,
    operation: SandboxConnectOperation,
    ownerId?: `tea-${string}`,
    command?: string,
  ): Promise<components["schemas"]["sandboxConnectResponse"]> {
    const { data, error, response } = await this.apiClient.POST(
      `/sandboxes/{sandboxId}/runs/{operation}/token`,
      {
        params: {
          path: {
            sandboxId,
            operation,
          },
          query: {
            ownerId: this.resolveOwnerId(ownerId),
          },
        },
        ...(command ? { body: { command } } : {}),
      },
    );
    if (error) {
      throw getTypedApiError(error, response, "Failed to get connect token");
    }
    return data;
  }

  private async getFileConnectToken(
    sandboxId: string,
    path: string,
    operation: SandboxFileOperation,
    ownerId?: `tea-${string}`,
  ): Promise<components["schemas"]["sandboxConnectResponse"]> {
    const { data, error, response } = await this.apiClient.POST(
      "/sandboxes/{sandboxId}/files/{operation}/token",
      {
        params: {
          path: { sandboxId, operation },
          query: {
            ownerId: this.resolveOwnerId(ownerId),
            path,
          },
        },
      },
    );
    if (error) {
      throw getTypedApiError(error, response, "Failed to get file connect token");
    }
    return data;
  }

  async exec(
    sandboxId: string,
    command: string,
    ownerId?: `tea-${string}`,
    signal?: AbortSignal,
  ): Promise<AsyncGenerator<SandboxExecEvent>> {
    if (signal?.aborted) {
      throw new AbortError();
    }

    const tokenResponse = await this.getRunConnectToken(sandboxId, "stream", ownerId, command);

    let response: Response;
    try {
      response = await fetch(tokenResponse.uri, {
        method: tokenResponse.method,
        headers: this.getStreamHeaders(tokenResponse.token),
        body: JSON.stringify({ command }),
        signal,
      });
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        throw new AbortError();
      }
      throw err;
    }

    if (!response.ok) {
      throw await getResponseError(response, "Failed to execute sandbox command");
    }
    if (!response.body) {
      throw new RenderError("Sandbox exec stream response did not include a response body.");
    }

    return this.iterExecEvents(response.body);
  }

  private async *iterExecEvents(
    body: ReadableStream<Uint8Array>,
  ): AsyncGenerator<SandboxExecEvent> {
    try {
      let sawTerminalEvent = false;
      for await (const event of parseSseStream(body)) {
        switch (event.event) {
          case "output": {
            const output = parseEventData<SandboxExecOutputEvent>(event);
            yield { type: "output", ...output };
            break;
          }
          case "exit": {
            const exit = parseEventData<SandboxExecExitEvent>(event);
            sawTerminalEvent = true;
            yield { type: "exit", ...exit };
            return;
          }
          case "error": {
            const streamError = parseEventData<SandboxExecErrorEvent>(event);
            sawTerminalEvent = true;
            throw new SandboxExecStreamError(streamError.status, streamError.message);
          }
          default:
            throw new RenderError(`Unknown sandbox exec stream event "${event.event}".`);
        }
      }
      if (!sawTerminalEvent) {
        throw new RenderError("Sandbox exec stream ended without a terminal event.");
      }
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        throw new AbortError();
      }
      throw err;
    }
  }

  private getStreamHeaders(connectToken: string): Record<string, string> {
    return {
      Accept: "text/event-stream",
      "Content-Type": "application/json",
      "User-Agent": getUserAgent(),
      Authorization: `Bearer ${connectToken}`,
    };
  }
}

type SseEvent = {
  event: string;
  data: string;
};

async function* parseSseStream(stream: ReadableStream<Uint8Array>): AsyncGenerator<SseEvent> {
  const reader = stream.getReader();
  try {
    const decoder = new TextDecoder();
    let buffer = "";
    let event = "";
    let data = "";

    const processLine = (line: string): SseEvent | null => {
      if (line === "") {
        if (!event && !data) {
          return null;
        }
        const complete = { event, data };
        event = "";
        data = "";
        return complete;
      }
      if (line.startsWith("event:")) {
        event = line.slice("event:".length).trim();
        return null;
      }
      if (line.startsWith("data:")) {
        if (data) {
          data += "\n";
        }
        data += line.slice("data:".length).replace(LEADING_SPACE, "");
      }
      return null;
    };

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      let newlineIndex = buffer.indexOf("\n");
      while (newlineIndex !== -1) {
        const line = buffer.slice(0, newlineIndex).replace(TRAILING_CARRIAGE_RETURN, "");
        buffer = buffer.slice(newlineIndex + 1);
        const complete = processLine(line);
        if (complete) {
          yield complete;
        }
        newlineIndex = buffer.indexOf("\n");
      }
    }

    buffer += decoder.decode();
    if (buffer) {
      const trailing = processLine(buffer.replace(TRAILING_CARRIAGE_RETURN, ""));
      if (trailing) {
        yield trailing;
      }
    }
    const complete = processLine("");
    if (complete) {
      yield complete;
    }
  } finally {
    await reader.cancel().catch(() => {});
    reader.releaseLock();
  }
}

function parseEventData<T>(event: SseEvent): T {
  try {
    return JSON.parse(event.data) as T;
  } catch (err) {
    const reason = err instanceof Error ? err.message : String(err);
    throw new RenderError(`Failed to parse sandbox exec "${event.event}" event data: ${reason}`);
  }
}

async function getResponseError(response: Response, context: string): Promise<Error> {
  const text = await response.text();
  return getApiError(text || response.statusText, response, context);
}

function getTypedApiError(error: unknown, response: Response, context: string): Error {
  const message =
    typeof (error as { message?: unknown })?.message === "string"
      ? (error as { message: string }).message
      : JSON.stringify(error);
  return getApiError(message, response, context);
}
