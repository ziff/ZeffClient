.POSIX:
.PHONY: install publish docs examples validate build test lint help

PIP           = python -m pip
PIPFLAGS      = --quiet

install:			## Install system
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e .
	python setup.py install


publish:			## Publish the library to the central PyPi repository
	echo python setup.py sdist upload


docs:				## Create documentation
	@echo Update required tools
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[docs]"
	@echo Create documentation
	@$(MAKE) -C docs docs


examples:			## Setup environement for doing examples
	@${PIP} ${PIPFLAGS} install --upgrade pip
	@${PIP} ${PIPFLAGS} install --upgrade -e .
	@${PIP} ${PIPFLAGS} install --upgrade -e ".[examples]"
	python setup.py build install


validate: lint test	## Validate project for CI, CD, and publish


clean:				## Clean generated files
	@rm -rf build
	@rm -rf dist
	@rm -rf sdist
	@rm -rf var
	@rm -rf tmp
	@rm -rf .eggs
	@rm -rf *.egg-info
	@rm -rf pip-wheel-metadata
	@find zeff -name '__pycache__' -exec rm -rf {} \; -prune
	@$(MAKE) -C docs clean


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
	python setup.py build


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

