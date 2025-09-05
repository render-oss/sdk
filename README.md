# workflow-sdk
An SDK for Render's workflow product

# Development

To install pre-commit hooks, run:

```bash
pre-commit install
pre-commit autoupdate
```

## API Documentation

To view API documentation from the OpenAPI spec:

```bash
npx @redocly/cli preview-docs openapi/openapi.yaml
```

# Tilt

Run tilt on a separate port to avoid conflicting with the main Tilt.

```
tilt up --port 10351
```

Tilt dev will build the example app and inject it into a Workflows DaemonSet. The DaemonSet has a configured workflow service ID and workflow version ID.

You should update the namespace to an already created namespace that also contains the `gcr-docker-config` secret. This Tiltfile expects your machine to be able to push gcr.io/render-devs/workflow-sdk-dev. When in doubt, create a Postgres in your desired workspace.

Once we get Workflow deploys working with the scheduler/renderd, we can drop this Tiltfile and friends.
