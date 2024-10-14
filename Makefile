## -*- mode: make -*-

# project specific
PROJECT        := pato-gui
BRANCH 	 	     := main
PYTHON_VERSION := 3.10
DEVBOX         := devbox
POETRY_OPTIONS := --no-ansi 
POETRY         := $(DEVBOX) run -- poetry $(POETRY_OPTIONS)
PYTHON 	       := $(POETRY) run python
PIP    	       := $(POETRY) run pip
PYTEST 	       := $(POETRY) run pytest
GIT 			     := git
# Otherwise perl may complain on a Mac
LANG           := C
# Must be invoked dynamic, i.e. the environment may not be ready yet
VERSION         = $(shell $(POETRY) version -s)
# Idem
TAG 	          = v$(VERSION)

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

all: init install pato-gui-build  ## Do it all: initialize, install and build the executable

init: ## Fulfill the requirements
	$(POETRY) build

install: init ## Install the package to the Python installation path.
	$(POETRY) lock
	$(POETRY) install

pato-gui: install ## Run the PATO GUI
	$(POETRY) run $@

pato-gui-build: install ## Build the PATO GUI exectable
	$(POETRY) run $@

test: install ## Test the package.
	$(POETRY) check
	$(POETRY) run pytest

dist: install test ## Prepare the distribution the package by installing and testing it.

upload_test: dist ## Upload the package to PyPI test.
	$(POETRY) publish -r test-pypi

upload: dist ## Upload the package to PyPI.
	$(POETRY) publish

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"

clean: ## Cleanup the environment
	$(GIT) clean -d -x -i

.PHONY: help \
				all \
				env-create \
				env-export \
