MAKEFLAGS   += --silent --stop
ROOT_DIR 	:= $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
TESTS_DIR	:= $(ROOT_DIR)/tests

PYTESS_ARGS += tests
PYTEST_ARGS	+= -rx --tb=short --quiet

-include local.mk

deps:
	pip install --upgrade -r requirements.txt

.PHONY: test-spec
test-spec:
	pytest $(TESTS_DIR)/test_helm_release.py $(PYTEST_ARGS) $(ARGS)

.PHONY: test-yaml
test-yaml:
	pytest $(TESTS_DIR)/test_yaml_files.py $(PYTEST_ARGS) $(ARGS)

.PHONY: tests
tests:
	pytest $(TESTS_DIR) $(PYTEST_ARGS) $(ARGS)