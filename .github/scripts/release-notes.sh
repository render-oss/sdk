#!/usr/bin/env bash
# Prints the GitHub release notes for a release tag, like python/v1.6.0: the
# section for that version in <language>/CHANGELOG.md, then a link that
# compares the tag with the previous release tag of the same language.
#
# Usage: release-notes.sh <tag>
#
# Fails if the changelog has no section for the version. Run it from the
# repository root, with all tags fetched. The tag itself does not have to
# exist yet.
set -o errexit -o nounset -o pipefail

tag="$1"
language="${tag%%/*}"
version="${tag#*/v}"
changelog="$language/CHANGELOG.md"

# Print the lines after "## [<version>]" until the next "## [" heading, and
# skip the blank lines at the start.
notes="$(awk -v heading="## [$version]" '
  index($0, heading) == 1 { found = 1; next }
  found && /^## \[/ { exit }
  found && !started && /^[[:space:]]*$/ { next }
  found { started = 1; print }
' "$changelog")"

if [[ -z "$notes" ]]; then
  echo "$changelog has no section for $version." >&2
  exit 1
fi

printf '%s\n' "$notes"

# The tag before this one in version order. It is empty for the first
# release. The tag is added to the list because the release workflows create
# it after they write the notes.
previous="$({ git tag --list "$language/v[0-9]*"; echo "$tag"; } | sort -V -u | grep -F -x -B1 "$tag" | grep -F -x -v "$tag" || true)"
if [[ -n "$previous" ]]; then
  printf '\n**Full Changelog**: https://github.com/%s/compare/%s...%s\n' \
    "$GITHUB_REPOSITORY" "$previous" "$tag"
fi
