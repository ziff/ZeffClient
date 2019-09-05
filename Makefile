.POSIX:
.PHONY: install publish docs examples validate build test lint help

SETUP         = python -m setup
SETUPFLAGS    =
PIP           = python -m pip
PIPFLAGS      = --quiet

install:			## Install system
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e .
	${SETUP} ${SETUPFLAGS} install


# Publish requires a username & password for twine to upload to PyPI
# ``export TWINE_USERNAME=<username>``
# ``export TWINE_PASSWORD=<password>``
#
# For automated upload with API token the following is required:
# ``export TWINE_USERNAME=__token__``
# ``export TWINE_PASSWORD=pypi-<token_value>``
publish: clean		## Publish the library to the central PyPi repository
	@${PIP} ${PIPFLAGS} install --upgrade pip setuptools wheel twine
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[docs]"
	${SETUP} ${SETUPFLAGS} sdist bdist_wheel
	python -m twine check dist/*
	python -m twine upload --verbose dist/*
	@$(MAKE) -C docs publish


docs:				## Create documentation
	@echo Update documentation tools
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[docs]"
	@echo Create documentation
	@$(MAKE) -C docs docs


examples:			## Setup environement for doing examples
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e .
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[examples]"
	${SETUP} ${SETUPFLAGS} build install


validate: lint test	## Validate project for CI, CD, and publish


clean:				## Clean generated files
	@$(MAKE) -C docs clean
	@rm -rf build
	@rm -rf dist
	@rm -rf sdist
	@rm -rf var
	@rm -rf tmp
	@rm -rf .eggs
	@rm -rf *.egg-info
	@rm -rf pip-wheel-metadata
	@find zeff -name '__pycache__' -exec rm -rf {} \; -prune


clean_cache:		## Clean caches
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -rf coverage_html_report
	@rm -rf .mypy_cache
	@rm -rf .hypothesis


build:				## Build into ``./build`` directory
	@echo Updating build tools
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e .
	${SETUP} ${SETUPFLAGS} build


test:				## Run test suite
	@echo Updating test tools
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[tests]"
	python -m pytest --cov=zeff && \
		coverage html


lint:				## Check source for conformance
	@echo Checking source conformance
	@echo Updating lint tools
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[lint]"
	pylint -f parseable -r n zeff
	pycodestyle zeff
	pydocstyle zeff
	mypy zeff


format:				## Format source code to standard
	@echo Formatting source
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[dev]"
	find zeff -name '*.py' -exec black -q {} \;
	find tests -name '*.py' -exec black -q {} \;


updatedev:			## Update / init all packages for development environment
	${PIP} ${PIPFLAGS} install --upgrade pip
	${PIP} ${PIPFLAGS} install --upgrade -e .
	${PIP} ${PIPFLAGS} install --upgrade -e ".[dev]"
	${PIP} ${PIPFLAGS} install --upgrade -e ".[tests]"
	${PIP} ${PIPFLAGS} install --upgrade -e ".[lint]"
	${PIP} ${PIPFLAGS} install --upgrade -e ".[docs]"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

