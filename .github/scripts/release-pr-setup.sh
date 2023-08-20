#!/bin/bash

deployment="$1"
environment="$2"
sha="$3"
repo_url="$4"
github_tag="$5"

if [[ -n "${repo_url}" ]] && [[ -n "${github_tag}" ]]
then
    echo "PR_BODY<<EOF" >> $GITHUB_ENV
    echo "## [${github_tag}]($(gh release view ${github_tag} --repo ${repo_url} --json url -q .url))
    " >> $GITHUB_ENV
    echo "$(gh release view ${github_tag} --repo ${repo_url} --json body -q .body)" >> $GITHUB_ENV
    echo "EOF" >> $GITHUB_ENV
else
    echo "PR_BODY=Releasing ${deployment} ${sha} to ${environment}" >> $GITHUB_ENV
fi

echo "PR_TITLE=[${environment}] Release ${deployment} ${sha}" >> $GITHUB_ENV
echo "PR_COMMIT_MESSAGE=gitops(${environment}): Update ${deployment} to ${sha}" >> $GITHUB_ENV
echo "PR_BRANCH=gitops/${environment}/${deployment}-${sha}" >> $GITHUB_ENV
