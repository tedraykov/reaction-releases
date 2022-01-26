HELM_CHARTS   = $(shell helm-toolkit list-charts --missing)
HELM_PACKAGES = $(wildcard packages/*.tgz)

-include local.mk

# repo-add: add repository
.PHONY: repo-add
repo-add:
	helm repo add $(HELM_REPOSITORY_NAME) $(HELM_REPOSITORY_URL)

# charts/%: build package .tgz from charts directory
charts/%: .FORCE
	helm package --destination packages $@ $(ARGS)

# list-missing: compare index.yaml against local charts directory
.PHONY: list-missing
list-missing:
	helm-toolkit list-charts --missing $(ARGS)

# packages/%.tgz: upload helm packages to S3 bucket
packages/%.tgz: .FORCE
	helm s3 push $@ $(HELM_REPOSITORY_NAME)

# packages: build helm packages
.PHONY: packages
packages: $(HELM_CHARTS)
	helm s3 reindex $(HELM_REPOSITORY_NAME)

# plugins: install helm plugins
.PHONY: plugins
plugins:
	helm plugin add https://github.com/hypnoglow/helm-s3||true
	helm plugin list

# publish: regenerate index.yaml in S3 bucket
.PHONY: publish
publish: $(HELM_PACKAGES)
	helm s3 reindex $(HELM_REPOSITORY_NAME)
