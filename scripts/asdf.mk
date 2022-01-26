ASDF_DIR      ?= ~/.asdf
ASDF_DATA_DIR ?= ~/.asdf
ASDF_PLUGINS   = $(shell egrep -o '^[a-z-]+' .tool-versions)
MAKEFLAGS     += --silent

asdf = $(shell which asdf $(ASDF_DIR)/bin/asdf|head -1)

.DEFAULT_GOAL := all

.PHONY: all
all: debug clone plugins install

$(ASDF_DIR):
	git clone --single-branch https://github.com/asdf-vm/asdf.git $@

$(ASDF_DATA_DIR)/plugins/%:
	$(asdf) plugin-add $(notdir $@)

.PHONY: clone
clone: $(ASDF_DIR)

.PHONY: install
install:
	$(asdf) install

.PHONY: plugins
plugins: $(addprefix $(ASDF_DATA_DIR)/plugins/, $(ASDF_PLUGINS))
	echo "ASDF_PLUGINS: $(ASDF_PLUGINS)"

.PHONY: debug
debug:
	echo ASDF_BIN: $(asdf)
	echo ASDF_DATA_DIR: $(ASDF_DATA_DIR)
	echo ASDF_DIR: $(ASDF_DIR)
