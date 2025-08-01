checkfiles = aiopathlib/__init__.py tests/test_async.py tests/test_sync.py
.PHONY: lint 
.DEFAULT_GOAL := help
help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

up: ## Update dependencies
	uv lock --upgrade

sync:
	uv sync --all-groups --all-extras $(options)

deps:
	$(MAKE) sync options="--frozen --inexact"

build:  ## Build wheel and zip
	uv build

publish: build
	twine check dist/*
	twine upload dist/*

style: ## Auto-formats the code
	ruff format $(checkfiles)
	ruff check --fix $(checkfiles)

lint: ## Reformat with isort and black, then check style with flake8 and mypy
	$(MAKE) style
	mypy $(checkfiles)

check: build  ## Checks that build is sane
	ruff format --check $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	ruff check $(checkfiles)
	mypy $(checkfiles)
	bandit -c pyproject.toml -r .
	twine check dist/*

test: ## Test code with pytest and show coverage
	coverage run -m pytest
	coverage report -m

part = patch

bump: ## Bump up version
	fast bump $(part)  # major/minor/patch
	git log -3
