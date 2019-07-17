# SDI GitOps™ Releases

## Overview

This repo contains our deployment automation for SDI's Reaction Commerce instances. The tech stack is centered around kubernetes helm charts as the main thing, weave flux as the gitops engine, and augmented with some specialized extras like the strimzi operator for kafka.

The companion repository is [reactioncommerce/reaction-infrastructure](https://github.com/reactioncommerce/reaction-infrastructure) which is focused on the base infrastructure layer (k8s cluster, monitoring, elasticsearch, etc), whereas this "sdi-releases" repo is focused on the application itself.

**How It Works™ High Level**

The files in this repo declare a desired state of the full distributed system which includes: which version of code, all the environment variable configuration, some networking, logging, etc. You cause change to the deployed system by creating a pull request against this repository. When your pull request is merged, the weave flux gitops code will roll out changes to make the running system match the new declared state.

To get a change at a high level you:

- clone this repo
- pull the latest develop and make a feature branch
- edit files (details below)
- open a pull request and get it review
- once the PR merges, your changes get deployed

## Developer How Tos With Detail

### How to update reaction core

- Find the git commit hash of the version you want to deploy
  - Typically this is the most recent commit on the default branch

```sh
cd reaction
git ls-remote --symref origin develop | awk '{print $1}'
```

Make a PR to this repo as follows.

- Start with your normal PR git mechanics (pull latest, create branch)
- edit **ALL** of the files that apply to your target deployment
  - staging: `sdi-bobs/staging/application/releases/reaction-core-*.yaml`
  - production: `sdi-bobs/production/application/releases/reaction-core-*.yaml`
- Edit the `yaml` file to change the nested key at `spec.values.image.tag` so it has the new commit sha you just found, which is a line that will look like this
  - `      tag: d8219e812ccfb7064af1628fb847096eeab29c4d`
- Commit, push, open PR, request review as normal

### How to update storefront

- Find the git commit hash of the version you want to deploy
  - Typically this is the most recent commit on the default branch

```sh
cd storefront
git ls-remote --symref origin develop | awk '{print $1}'
```

Make a PR to this repo as follows.

- Start with your normal PR git mechanics (pull latest, create branch)
- edit the file that applies to your target deployment
  - staging: `sdi-bobs/staging/application/releases/reaction-storefront.yaml`
  - production: `sdi-bobs/production/application/releases/reaction-storefront.yaml`
- Edit the `yaml` file to change the nested key at `spec.values.image.tag` so it has the new commit sha you just found, which is a line that will look like this
  - `      tag: d8219e812ccfb7064af1628fb847096eeab29c4d`
- Commit, push, open PR, request review as normal
