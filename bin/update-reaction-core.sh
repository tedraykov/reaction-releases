#!/usr/bin/env bash

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
stores=("bobs" "ems")
for store in ${stores[*]} ; do
  find "sdi-${store}/${deployment}/application/releases" -type f -name "reaction-core-*.yaml" -print0 |
    xargs -0 perl -pi -e "s,^\s+tag:.*,      tag: ${new_tag},"
done