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

get_tag() {
  grep -E '^\s+tag:' "$1" | cut -d : -f 2- | tr -d "' " | tr -d '"' || true
}

main() {
  cd "$(dirname "${BASH_SOURCE[0]}")/.."

  local target_dir

  PS3='Which fascia would you like to promote? '
  select dir in sdi-*/ Quit
  do
      if [[ $dir == Quit ]]
      then
          exit 0
      fi
      target_dir="$dir"
      break
  done

  find "./${target_dir}/staging/application/releases" -type f -name "*.yaml" | {
    while IFS= read -r from_path; do
      from_tag=$(get_tag "${from_path}")
      if [[ -z "${from_tag}" ]]; then
        continue
      fi
      to_path="${from_path/staging/production}"
      if [[ ! -f "${to_path}" ]]; then
        continue
      fi
      to_tag=$(get_tag "${to_path}")
      if [[ "${from_tag}" != "${to_tag}" ]]; then
        base=$(basename "${to_path}")
        echo "${base} from ${to_tag} -> ${from_tag}"
        # https://superuser.com/a/421707/34245
        read -n 1 -s -p "Promote? (y/N): " confirm </dev/tty
        echo
        confirm=$(echo "${confirm}" | tr A-Z a-z)
        if [[ "${confirm}" == "y" ]]; then
          perl -pi -e "s,^\s+tag:.*,      tag: '${from_tag}'," "${to_path}"
        fi
      fi
    done
  }
}

main "$@"
