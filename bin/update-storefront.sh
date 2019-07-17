#!/usr/bin/env bash

# This script tries to edit the spec.values.image.tag nested property of
# a helm chart yaml release file.

# Please Use Google Shell Style: https://google.github.io/styleguide/shell.xml

# ---- Start unofficial bash strict mode boilerplate
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -o errexit  # always exit on error
set -o errtrace # trap errors in functions as well
set -o pipefail # don't ignore exit codes when piping output
set -o posix    # more strict failures in subshells
# set -x          # enable debugging

IFS=$'\n\t'
# ---- End unofficial bash strict mode boilerplate

cd "$(dirname "${BASH_SOURCE[0]}")/.."
deployment="$1"
new_tag="$2"


find "sdi-bobs/${deployment}/application/releases" -type f -name "reaction-storefront*.yaml" -print0 |
  xargs -0 sed -Ei "s,^\s+tag:.*,      tag: ${new_tag},"
