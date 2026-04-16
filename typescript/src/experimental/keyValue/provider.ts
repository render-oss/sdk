import type {
  RedisClientType,
  RedisDefaultModules,
  RedisFunctions,
  RedisModules,
  RedisScripts,
  RespVersions,
  TypeMapping,
} from "redis";
import { createClient } from "redis";
import { RenderError } from "../../errors";
import type { KeyValueApi } from "./api";
import type {
  ConnectionInfo,
  KeyValueDetail,
  NameOwnerIdOptions,
  Options,
  OwnerId,
  RedisConfig,
  ServiceIdOptions,
} from "./types";
import { formatErrorMessage } from "./utils";

const connectionRE = /rediss?:\/\/(([\w-]+):([\w]+)@)?([\w.-]+):([0-9]+)/;
const maxDelayMS = 512 * 1000; // 512 seconds to line up with exponential backoff, ~8.5 minutes

/**
 * Provider for connecting to Render Key Value instances. Allows searching by name or by service
 * ID.
 */
export class KeyValueProvider {
  private readonly defaultOwnerId?: OwnerId;

  constructor(
    private readonly api: KeyValueApi,
    defaultOwnerId?: string,
  ) {
    this.defaultOwnerId = defaultOwnerId as OwnerId | undefined;
  }

  /**
   * Create a new client to connect to a given Render Key Value service.
   *
   * If searching by Name and there are no instances with that name in the given workspace, then
   * one will be automatically created using the configuration provided in `options`. To disable
   * this behavior, set `autoProvisionEnabled: false` in the `options` when calling this function.
   *
   * @param options Render Key Value options for locating the appropriate instance
   * @param redisConfig Additional settings to pass through to the Redis client
   * @returns A configured (but not yet connected) `node-redis` client, set up to connect to
   * the Render Key Value instance
   *
   * @example
   * ```typescript
   * import { Render } from "@renderinc/sdk";
   *
   * const render = new Render();
   * const client = await render.experimental.keyValue.newClient({
   *   name: "my-redis",
   * });
   * const conn = await client.connect();
   *
   * await conn.set("key", "value");
   * const value = await conn.get("key");
   *
   * conn.destroy();
   * ```
   */
  public async newClient<
    M extends RedisModules,
    F extends RedisFunctions,
    S extends RedisScripts,
    RESP extends RespVersions,
    TYPE_MAPPING extends TypeMapping,
  >(
    options: Options,
    redisConfig?: RedisConfig<M, F, S, RESP, TYPE_MAPPING>,
  ): Promise<RedisClientType<RedisDefaultModules & M, F, S, RESP, TYPE_MAPPING>> {
    const url = await this.loadConnectionString(options);

    return createClient({ url, ...redisConfig });
  }

  /**
   * Get connection information for a given Render Key Value service
   *
   * If searching by Name and there are no instances with that name in the given workspace, then
   * one will be automatically created using the configuration provided in `options`. To disable
   * this behavior, set `autoProvisionEnabled: false` in the `options` when calling this function.
   *
   * @param options Render Key Value options for locating the appropriate instance
   * @returns An object with the connection information needed to connect
   *
   * @example
   * ```typescript
   * import { Render } from "@renderinc/sdk";
   *
   * const render = new Render();
   * const connectionString = await render.experimental.keyValue.connectionInfo({
   *   name: "my-redis",
   * }); // { host: "my.redis.url", port: 1234 }
   * ```
   */
  public async connectionInfo(options: Options): Promise<ConnectionInfo> {
    const connectionString = await this.loadConnectionString(options);

    return parseConnectionString(connectionString);
  }

  private async loadConnectionString(options: Options): Promise<string> {
    let details: KeyValueDetail;

    if (hasServiceId(options)) {
      details = await this.findInstanceByServiceId(options);
    } else {
      details = await this.findInstanceByNameOwnerId(options);
    }

    return await this.api.getConnectionInfo(details.id);
  }

  private async findInstanceByServiceId(options: ServiceIdOptions): Promise<KeyValueDetail> {
    return await this.api.findById(options.serviceId);
  }

  private async findInstanceByNameOwnerId(options: NameOwnerIdOptions): Promise<KeyValueDetail> {
    const ownerId = this.resolveOwnerId(options.ownerId);
    const details = await this.api.findByName(options.name, ownerId);

    if (!details) {
      if (options.autoProvisionEnabled === false) {
        const message = formatErrorMessage(
          `Unable to locate Key Value named '${options.name}'`,
          `Please double-check that the name is correct.
If you would like one to be created automatically, ensure that 'autoProvisionEnabled' is not set to 'false'.`,
        );
        throw new RenderError(message);
      } else {
        return this.provisionNewInstance(ownerId, options);
      }
    }

    return details;
  }

  private async provisionNewInstance(
    resolvedOwnerId: OwnerId,
    options: NameOwnerIdOptions,
  ): Promise<KeyValueDetail> {
    const data = await this.api.createInstance({
      name: options.name,
      ownerId: resolvedOwnerId,
      plan: options.plan ?? "free",
      maxmemoryPolicy: options.maxmemoryPolicy,
      ipAllowList: options.ipAllowList,
    });

    return await this.waitForInstanceAvailable(data.id);
  }

  private async waitForInstanceAvailable(keyValueId: string): Promise<KeyValueDetail> {
    let retryDelay = 1000;

    while (retryDelay <= maxDelayMS) {
      let data: KeyValueDetail;
      try {
        data = await this.api.findById(keyValueId);
      } catch (_err) {
        const message = formatErrorMessage(
          "Unable to look up status information about Key Value instance.",
          "This is most likely a Render error, please try again.",
        );
        throw new RenderError(message);
      }

      switch (data.status) {
        case "available":
          // The instance is ready, so we're done waiting
          return data;
        case "creating":
        case "config_restart":
        case "updating_instance":
          // The instance is still being updated / created, so we should wait and try again
          await new Promise((resolve) => setTimeout(resolve, retryDelay));
          break;
        default: {
          // If we're in any other state, the instance isn't available and we don't expect it to
          // become available, so error out
          const message = formatErrorMessage(
            "The requested Key Value instance is not available.",
            "Please view the Key Value on dashboard.render.com to verify its status.",
          );
          throw new RenderError(message);
        }
      }

      // Double the retry delay each time so that we don't spam the API
      retryDelay *= 2;
    }

    const message = formatErrorMessage(
      "Timed out waiting for instance to become available.",
      "Please check the Key Value on dashboard.render.com to make sure it is ready, then try again.",
    );

    throw new RenderError(message);
  }

  private resolveOwnerId(ownerId?: OwnerId): OwnerId {
    const resolved = ownerId || this.defaultOwnerId;
    if (!resolved) {
      throw new RenderError(
        "ownerId is required. Provide it as a parameter or set the RENDER_WORKSPACE_ID environment variable.",
      );
    }
    return resolved;
  }
}

function hasServiceId(options: Options): options is ServiceIdOptions {
  return (options as ServiceIdOptions).serviceId !== undefined;
}

function parseConnectionString(connection: string): ConnectionInfo {
  const matches = connection.match(connectionRE);

  if (!matches) {
    const message = formatErrorMessage(
      "The Key Value connection string returned from the server was in an unexpected format",
      "Please confirm you are on the most recent version of the Render SDK",
    );
    throw new RenderError(message);
  }

  return {
    username: matches[2],
    password: matches[3],
    host: matches[4],
    port: Number(matches[5]),
  };
}
