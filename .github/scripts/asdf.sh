#!/bin/bash -e
ASDF_DIR=~/.asdf
echo ASDF_DIR=$ASDF_DIR >> $GITHUB_ENV
echo "${ASDF_DIR}/bin" >> $GITHUB_PATH
echo "${ASDF_DIR}/shims" >> $GITHUB_PATH
