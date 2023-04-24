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
# Create a map of the deployment name and a list of all deployments matching that name

cd "$(dirname "${BASH_SOURCE[0]}")/.."
deployment="$1"
stage="$2"
new_tag="${3:0:7}"
stores=("bobs" "ems")
for store in ${stores[*]} ; do
  if [[ $deployment = "reaction-core" ]]
  then
  find "sdi-${store}/${stage}/application/releases" -type f -name "reaction-storefront.yaml" -print0 |
    xargs -0 perl -pi -e "s,^\s+tag:.*,      tag: ${new_tag},"
  elif [[ $deployment = "storefront" ]]
  then
  find "sdi-${store}/${stage}/application/releases" -type f -name "reaction-storefront.yaml" -print0 |
    xargs -0 perl -pi -e "s,^\s+tag:.*,      tag: ${new_tag},"
  elif [[ $deployment = "reaction-sftp-to-s3-order-status" ]]
  then
  find "sdi-${store}/${stage}/application/releases" -type f -name "reaction-sftp-to-s3-order-status.yaml" -print0 |
    xargs -0 perl -pi -e "s,^\s+version:.*,      version: ${new_tag},"
  elif [[ $deployment = "reaction-etl-rom-order-status-import" ]]
  then
  find "sdi-${store}/${stage}/application/releases" -type f -name "reaction-etl-rom-order-status-import.yaml" -print0 |
    xargs -0 perl -pi -e "s,^\s+version:.*,      version: ${new_tag},"
  fi
done
