# Releasing the Render SDK

> [!IMPORTANT]
> This file is internal. It is deliberately excluded from the public
> `render-oss/sdk` mirror by `copy.bara.sky`; see [Keeping this file
> internal](#keeping-this-file-internal) before moving or renaming it.

Releasing the Python and Typescript SDKs is a manual process - follow the steps below to cut a new release!

## Access you need first

- **PyPI**: the API token in 1Password, "Python SDK Release Publish API Token
  (PyPi)". If it has expired, log into the
  `render-oss` PyPI organization with the 1Password credentials and generate a
  new one.
- **npm**: membership in the `@renderinc` organization. Ask in #help-it.
- **GitHub**: membership in the
  [render-oss dev team](https://github.com/orgs/render-oss/teams/dev), which is
  what lets you push tags and cut releases on the public mirror. Ask in
  #help-it.

Add the public mirror as a second remote:

```bash
git remote add oss git@github.com:render-oss/sdk.git
```

## Ordering

In general we should design SDK changes to be backwards compatible with our API - it is safer to expand a client side type than it is to restrict a type. 

This is especially notable for Python, where we use `openapi-python-client` which generates strict enums that raise `ValueError` on unknown values.

## Changelog convention

Incremental PRs are not required to add CHANGELOG entries. Instead we populate the notes for the current release as part of the release process. Start by reading the commits and PRs since the previous tag for each language and backfilling the notes.

## Python

We publish two packages for the Python SDK:

| Directory             | Distribution | Notes                                            |
| --------------------- | ------------ | ------------------------------------------------ |
| `python/`             | `render`     | The real SDK                                     |
| `python-metapackage/` | `render_sdk` | Deprecated shim for the pre-rename package name  |

There are tests to assert the two versions match - CI should yell at us if they're out of sync.

### 1. Bump the version

In `python/`:

- `pyproject.toml`: `version`
- `render/__init__.py`: `__version__`
- `CHANGELOG.md`: new section
- `uv.lock`: refresh with `uv lock`

Then regenerate the metapackage, which syncs its own version and its
`render==X.Y.Z` pins:

```bash
cd python-metapackage
uv run python scripts/generate_mirror.py
uv lock
```

`tests/test_import_matrix.py` and `tests/test_metadata.py` hardcode the
expected version string. The generator does not touch them, so update them by
hand or `python-metapackage-ci` fails.

Open the PR ([example](https://github.com/renderinc/sdk/pull/183)), merge to
`main`, and wait for copybara to sync it to
[render-oss/sdk](https://github.com/render-oss/sdk/).

### 2. Build and publish both distributions

```bash
cd python && uv build && uv publish --token pypi-XXX
cd ../python-metapackage && uv build && uv publish --token pypi-XXX
```

Verify [pypi.org/project/render](https://pypi.org/project/render/) and
[pypi.org/project/render-sdk](https://pypi.org/project/render-sdk/).

To rehearse against TestPyPI first (reset periodically, creds in
[1Password](https://start.1password.com/open/i?a=EKVF24RWFFAPZJZKVV4HN7AVJY&v=zvboai4y7qvq4e3hojy5rq5wxu&i=xg4fzrhius63qdo4spgnprvifq&h=render.1password.com)):

```bash
uv publish --token pypi-XXX --publish-url https://test.pypi.org/legacy/
```

### 3. Tag and cut the public release

Push a release tag to both repos, and publish a GitHub release on the render-oss side.

```bash
git tag -a python/vX.Y.Z -m "Python SDK vX.Y.Z"
git push origin python/vX.Y.Z
git push oss python/vX.Y.Z

gh release create python/vX.Y.Z \
  --repo render-oss/sdk \
  --title "Python SDK vX.Y.Z" \
  --notes-file notes.md
```

Release notes consist of the changelog for that release plus a link to CHANGELOG.md. You may find that using a
temp file is easier than quoting markdown on the command line.

## TypeScript

### 1. Bump the version

- `package.json`: `version`
- `CHANGELOG.md`: new section
- `package-lock.json`: refresh with `npm install`

Confirm `npm run build` and `npm test` pass. Open the PR
([example](https://github.com/renderinc/sdk/pull/184)), merge to `main`, and
wait for copybara to sync.

### 2. Publish to npm

```bash
cd typescript
npm run build
npm login
npm publish --access public
```

### 3. Tag and cut the public release

```bash
git tag -a typescript/vX.Y.Z -m "TypeScript SDK vX.Y.Z"
git push origin typescript/vX.Y.Z
git push oss typescript/vX.Y.Z

gh release create typescript/vX.Y.Z \
  --repo render-oss/sdk \
  --title "TypeScript SDK vX.Y.Z" \
  --notes-file notes.md
```

## Go

The Go SDK is internal only and is not published to a registry. A release is just a git tag:

```bash
git tag go/v0.1.0 <commit>
git push origin go/v0.1.0
```

## Keeping this file internal

`copy.bara.sky` mirrors only the paths in `DESTINATION_FILES` to
`render-oss/sdk`. Root-level files are listed one by one, so a new root file is
private by default; `RELEASING.md` is also named in `DESTINATION_FILES_EXCLUDE`
so the intent survives someone later broadening the include globs.

- Do not link to this file from `README.md`, or from anything else under
  `python/`, `typescript/`, `go/`, or `.github/`. Those are mirrored, and the
  link would 404 for the public.
- The `pr` workflow uses the same glob, so a public PR cannot modify this file
  on the way in.
