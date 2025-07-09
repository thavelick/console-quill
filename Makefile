# Sane defaults
SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# ---------------------- COMMANDS ---------------------------
dev: # Start console-quill server for development
	@echo "Starting console-quill server for development.."
	uv run python -m console_quill.server --logfile test.log --port 9876

install: # Install console-quill in development mode
	@echo "Installing console-quill in development mode.."
	uv tool install -e .

install-from-github: # Install from GitHub
	@echo "Installing from GitHub.."
	uv tool install git+https://github.com/thavelick/console-quill


clean: # Clean up test files
	@echo "Cleaning up test files.."
	rm -f test.log
	@echo "Done."

update: # Update dependencies
	@echo "Updating dependencies.."
	uv sync -U

lint: # Run ruff format and check with autofixing
	@echo "Running ruff format.."
	uv run ruff format
	@echo "Running ruff check with autofix.."
	uv run ruff check --fix



# -----------------------------------------------------------
# CAUTION: If you have a file with the same name as make
# command, you need to add it to .PHONY below, otherwise it
# won't work. E.g. `make run` wouldn't work if you have
# `run` file in pwd.
.PHONY: help

# -----------------------------------------------------------
# -----       (Makefile helpers and decoration)      --------
# -----------------------------------------------------------

.DEFAULT_GOAL := help
# check https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
NC = \033[0m
ERR = \033[31;1m
TAB := '%-20s' # Increase if you have long commands

# tput colors
red := $(shell tput setaf 1)
green := $(shell tput setaf 2)
yellow := $(shell tput setaf 3)
blue := $(shell tput setaf 4)
cyan := $(shell tput setaf 6)
cyan80 := $(shell tput setaf 86)
grey500 := $(shell tput setaf 244)
grey300 := $(shell tput setaf 240)
bold := $(shell tput bold)
underline := $(shell tput smul)
reset := $(shell tput sgr0)

help:
	@printf '\n'
	@printf '    $(underline)Available make commands:$(reset)\n\n'
	@# Print commands with comments
	@grep -E '^([a-zA-Z0-9_-]+\.?)+:.+#.+$$' $(MAKEFILE_LIST) \
		| grep -v '^env-' \
		| grep -v '^arg-' \
		| sed 's/:.*#/: #/g' \
		| awk 'BEGIN {FS = "[: ]+#[ ]+"}; \
		{printf "    make $(bold)$(TAB)$(reset) # %s\n", \
			$$1, $$2}'
	@grep -E '^([a-zA-Z0-9_-]+\.?)+:( +\w+-\w+)*$$' $(MAKEFILE_LIST) \
		| grep -v help \
		| awk 'BEGIN {FS = ":"}; \
		{printf "    make $(bold)$(TAB)$(reset)\n", \
			$$1}' || true
	@echo -e ""