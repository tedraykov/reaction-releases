MAKEFLAGS     += --silent --stop
PYTEST_ARGS   += -rx --tb=short --quiet
PACKAGES_PATH := packages

include scripts/helm.mk
-include local.mk

.DEFAULT_GOAL := all
.FORCE:

.PHONY: all
all: lint test

.uuidgen: .FORCE
	uuidgen > $@

.PHONY: deps
deps:
	pip3 install --upgrade -r requirements.txt $(ARGS)
	asdf reshim $(ARGS)

.PHONY: lint
lint:
	ct lint $(ARGS)

.PHONY: test
test:
	pytest $(PYTEST_ARGS) tests $(ARGS)

.PHONY: update-flux-chart
update-flux-chart:
	cd charts/flux && flux-chart-update --detect $(ARGS)
