import type {
  RedisClientOptions,
  RedisFunctions,
  RedisModules,
  RedisScripts,
  RespVersions,
  TypeMapping,
} from "redis";
import type { components } from "../../generated/schema";

export type KeyValueDetail = Omit<components["schemas"]["keyValueDetail"], "maintenance">;

interface ServiceId {
  serviceId: string;
}

interface NameOwnerId {
  name: string;
  ownerId?: OwnerId;
}

interface InstanceConfiguration {
  autoProvisionEnabled?: boolean;
}

export type ServiceIdOptions = ServiceId & InstanceConfiguration;
export type NameOwnerIdOptions = NameOwnerId & InstanceConfiguration;
export type Options = ServiceIdOptions | NameOwnerIdOptions;
export type RedisConfig<
  M extends RedisModules = RedisModules,
  F extends RedisFunctions = RedisFunctions,
  S extends RedisScripts = RedisScripts,
  RESP extends RespVersions = RespVersions,
  TYPE_MAPPING extends TypeMapping = TypeMapping,
> = Omit<
  RedisClientOptions<M, F, S, RESP, TYPE_MAPPING>,
  "url" | "socket" | "username" | "password"
>;

export type OwnerId = `tea-${string}` | `own-${string}`;

export interface ConnectionInfo {
  host: string;
  port: number;
  username?: string;
  password?: string;
}
