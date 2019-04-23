PYTESS_ARGS += tests
PYTEST_ARGS	+= -rx --tb=short --quiet

-include local.mk

deps:
	pip install --upgrade -r requirements.txt

.PHONY: test-spec
test-spec:
	pytest tests/test_helm_release.py $(PYTEST_ARGS) $(ARGS)

.PHONY: test-yaml
test-yaml:
	pytest tests/test_yaml_files.py $(PYTEST_ARGS) $(ARGS)

.PHONY: tests
tests:
	pytest tests $(PYTEST_ARGS) $(ARGS)
