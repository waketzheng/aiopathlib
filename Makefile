checkfiles = aiopathlib.py tests/test_async.py
black_opts = -l 88 -t py38
.PHONY: lint 
.DEFAULT_GOAL := help
help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

up: ## Update dependencies
	poetry update
	poetry export --dev --without-hashes >> dev_requirements.txt

build:  ## Build wheel and zip
	rm -fR dist/
	poetry build

publish: build
	twine upload dist/*

lint: ## Reformat with isort and black, then check style with flake8 and mypy
	isort $(checkfiles)
	black $(black_opts) $(checkfiles)
	flake8 $(checkfiles)
	mypy $(checkfiles)

check: build  ## Checks that build is sane
ifneq ($(shell which black),)
	black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
endif
	flake8 $(checkfiles)
	mypy $(checkfiles)
	#pylint -d C,W,R $(checkfiles)
	bandit -r $(checkfiles)
	twine check dist/*

style: ## Auto-formats the code
	autoflake --in-place --remove-all-unused-imports $(checkfiles)
	isort -src $(checkfiles)
	black $(black_opts) $(checkfiles)

test: ## Test code with pytest and show coverage
	coverage run -m pytest
	coverage report -m

bump: ## Bump up version
ifeq ($(shell which bumpversion),)
	pip install bumpversion
endif
	bumpversion patch  # major/minor/patch
	git log
