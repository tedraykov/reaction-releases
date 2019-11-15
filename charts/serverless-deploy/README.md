# Serverless Deploy Helm Chart

This directory contains a Kubernetes chart to deploy [Serverless Deploy](https://github.com/sportsdirect/reaction-serverless-deploy/) container.

## Chart Details

This chart will do the following:

* Create a job to run `serverless deploy`
* Create an optional sealed-secret resource when secrets are defined.

## Installing the Chart

```console
$ helm install serverless-deploy -n reaction-etl-catalog-sync -f values.yaml
```

## Configuration

The following table lists the configurable parameters of the serverless-deploy chart and their default values.

|          Parameter                   |                         Description                         |                   Default                                         |
| :----------------------------------- | :---------------------------------------------------------- | :---------------------------------------------------------------- |
| `annotations`                        | Annotations to add to the job resource                      | `{}`                                                              |
| `configMapRefs`                      | Reference to the existing ConfigMap to source               | `[ 'buckets', 'kafka', 'serverless-deploy' ]`                     |
| `environment`                        | Environment vars for serverless application                 | `{}`                                                              |
| `image.pullPolicy`                   | Container pull policy                                       | `Always`                                                          |
| `image.repository`                   | Container image to use                                      | `816897914983.dkr.ecr.us-east-1.amazonaws.com/serverless-deploy`  |
| `image.tag`                          | Container image tag to deploy                               | `nil`                                                             |
| `jobBackoffLimit`                    | Number of retries for failed job execution                  | `1`                                                               |
| `package.baseUrl`                    | A base URL to fetch serverless.zip package from             | `https://sdi-management-serverless-packages.s3.amazonaws.com`     |
| `package.name`                       | A name for serverless.zip package                           | `nil`                                                             |
| `package.version`                    | A semver or commit hash of the serverless.zip package       | `nil`                                                             |
| `secrets`                            | SealedSecrets encrypted environment vars                    | `{}`                                                              |
| `secretRefs`                         | Reference to the existing Secrets resources                 | `[]`                                                              |
| `serverless.debug`                   | Enable serverless debug mode                                | `false`                                                           |
