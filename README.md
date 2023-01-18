# Reaction GitOps™ Releases

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

### How to update reaction core in staging

- Find the git commit hash of the version you want to deploy
  - Typically this is the most recent commit on the default branch

```sh
cd reaction
git ls-remote --symref origin develop | awk '{print $1}'
```

Make a PR to this repo as follows.

- Start with your normal PR git mechanics (pull latest, create branch)
- Run the following with either `staging` or `production`

```sh
./bin/update-reaction-core.sh staging NEW_SHA_GOES_HERE
```

- Verify with `git diff` that nothing weird is changed by mistake
- commit, push, pull request, request review as normal
  - Commit message convention: `gitops: staging <component-name>`

### How to update storefront in staging

- Find the git commit hash of the version you want to deploy
  - Typically this is the most recent commit on the default branch

```sh
cd reaction
git ls-remote --symref origin develop | awk '{print $1}'
```

Make a PR to this repo as follows.

- Start with your normal PR git mechanics (pull latest, create branch)
- Run the one of the following with either `staging` or `production`

```sh
./bin/update-storefront.sh staging NEW_SHA_GOES_HERE

or 

./bin/update-reaction-core.sh staging NEW_SHA_GOES_HERE
```

- Verify with `git diff` that nothing weird is changed by mistake
- commit, push, pull request, request review as normal
  - Commit message convention: `gitops: staging <component-name>`

### How to promote from staging to production

Make a PR to this repo as follows.

- Start with your normal PR git mechanics (pull latest, create branch)
- Run `./bin/promote.sh`
- Answer the `y/n` prompts with `y` for any components you want to promote
- Verify with `git diff` that nothing weird is changed by mistake
- commit, push, pull request, request review as normal
  - Commit message convention: `gitops: production <component-name>`

## REACTION-STOREFRONT environment variables

Details on how to deploy new environment variables and how to update existing ones for the storefront.

#### Adding a new encrypted value variables to the configuration

- Add the key to the sealed secret template for the storefront
    - /charts/reaction-storefront/templates/sealedsecret.yaml
    - place the new key under `spec.encryptedData`


#### Adding a new plain text variable to the configuration

- Add the key to the sealed secret template for the storefront
    - `/charts/reaction-storefront/templates/configmap.yaml`
    - place the new key under `data`

#### Adding the values

For new encrypted or plain text variables, once they have been added to the proper place in sealed secrets or config map, add them to the values file.

- `/charts/reaction-storefront/values.yaml`
- place the new keys as a document under `config`

### Configuring actual values for a given environment

There are currently two environments you can configure, which are staging and production.  Once you have your variables setup as described above you can add the opertaional values with the steps below.

#### Encrypting values for an environment

Make sure you have `kubectl` and `kubeseal` installed on your machine. The versions below will work with the commands listed. For each store and each environment there are different keys used to encrypt the values. Make sure you are within the proper directory for your store/environment before attempting to encrypt the string.

```
$ kubectl version --short
Client Version: v1.25.0
$ kubeseal --version
kubeseal version: v0.19.3
```

1. `$ cd /< sdi-store-name >/< environment >/application/releases`
2. `$ source .envrc`
3. `$ echo "sensitiveValue" | make encrypt-string`
4. Copy the value that is output
5. Paste the output into the proper key in `/< sdi-store-name >/< environment >/application/releases/reaction-storefront.yaml` under `spec.values.config`

#### Plain text values

Paste the value into the proper key in `/< sdi-store-name >/< environment >/application/releases/reaction-storefront.yaml` under `spec.values.config`


