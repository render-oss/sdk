import type { Client } from "openapi-fetch";
import { ClientError, ServerError } from "../../errors";
import type { paths } from "../../generated/schema";
import type { KeyValueDetail, KeyValuePatch, KeyValuePost, OwnerId } from "./types";
import { formatErrorMessage, isRender } from "./utils";

/**
 * Level 2 wrapper for the auto-generated REST API client, tailored to Key Value use-cases
 */
export class KeyValueApi {
  constructor(private readonly client: Client<paths>) {}

  /**
   * Look up a Key Value instance using its Service ID
   * @param keyValueId Service ID (red-xyz) to look up
   * @returns Detailed information about the Key Value instance with the provided id
   */
  public async findById(keyValueId: string): Promise<KeyValueDetail> {
    const { data, error, response } = await this.client.GET("/key-value/{keyValueId}", {
      params: { path: { keyValueId } },
    });

    checkApiTokenError(response);

    if (response.status === 404) {
      const message = formatErrorMessage(
        `Unable to locate a Key Value with ID ${keyValueId}`,
        "Please double-check the ID is correct",
      );
      throw new ClientError(message, 404);
    }

    if (error) {
      throw unexpectedError(`fetching info about Key Value ${keyValueId}`, response, error);
    }

    return data;
  }

  /**
   * Look up a Key Value instance by name and owner ID
   * @param name The name of the Key Value instance
   * @param ownerId The ownerId (workspace ID) of the Key Value instance
   * @returns Detailed information about the Key Value instance, if found. `null` otherwise
   */
  public async findByName(name: string, ownerId: OwnerId): Promise<KeyValueDetail | null> {
    const { data, error, response } = await this.client.GET("/key-value", {
      params: {
        query: {
          name: [name],
          ownerId: [ownerId],
        },
      },
    });

    checkApiTokenError(response);

    if (error) {
      throw unexpectedError(
        `fetching information about Key Value named '${name}'`,
        response,
        error,
      );
    }

    if (data.length === 0) {
      // No instances exist with the requested name
      return null;
    }

    return data[0].keyValue;
  }

  /**
   * Find the connection string for a given Key Value instance
   * @param keyValueId The service ID for the Key Value instance
   * @returns Appropriate connection string to connect to the instance (internal if we're running
   * on Render, external otherwise)
   */
  public async getConnectionInfo(keyValueId: string): Promise<string> {
    const { data, error, response } = await this.client.GET(
      "/key-value/{keyValueId}/connection-info",
      {
        params: {
          path: {
            keyValueId,
          },
        },
      },
    );

    checkApiTokenError(response);

    if (error) {
      throw unexpectedError(
        `fetching connection information for Key Value ${keyValueId}`,
        response,
        error,
      );
    }

    if (isRender()) {
      return data.internalConnectionString;
    } else {
      return data.externalConnectionString;
    }
  }

  /**
   * Create a new Key Value instance, using the provided configuration settings
   * @param details Instance configuration used to create the new instance
   * @returns Details about the newly-created instance
   */
  public async createInstance(details: KeyValuePost): Promise<KeyValueDetail> {
    const { data, error, response } = await this.client.POST("/key-value", {
      body: details,
    });

    checkApiTokenError(response);

    if (error) {
      throw unexpectedError(`creating new Key Value named '${details.name}'`, response, error);
    }

    return data;
  }

  /**
   * Updates a Key Value instance to have new configuration settings
   * @param keyValueId Service ID for the instance to update
   * @param update Changes that need to be applied to the instance
   * @returns Details about the updated instance
   */
  public async updateInstance(keyValueId: string, update: KeyValuePatch): Promise<KeyValueDetail> {
    const { data, error, response } = await this.client.PATCH("/key-value/{keyValueId}", {
      params: {
        path: { keyValueId },
      },
      body: update,
    });

    checkApiTokenError(response);

    if (error) {
      throw unexpectedError(`updating Key Value ${keyValueId}`, response, error);
    }

    return data;
  }
}

function unexpectedError(
  operation: string,
  response: Response,
  error: any,
): ClientError | ServerError {
  const message = `Unexpected error while ${operation}`;
  if (response.status >= 500) {
    return new ServerError(message, response.status, error);
  } else {
    return new ClientError(message, response.status, error);
  }
}

function checkApiTokenError(response: Response) {
  if (response.status === 401) {
    const message = formatErrorMessage(
      "The provided Render API Token is not authorized.",
      "Please double-check the token is correct.",
    );
    throw new ClientError(message, 401);
  }
}
