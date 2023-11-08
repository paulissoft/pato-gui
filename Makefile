## -*- mode: make -*-

# project specific
PROJECT  := pato-gui
BRANCH 	 := main
PYTHON_VERSION := 3.12

GIT = git
MYPY = mypy
# Otherwise perl may complain on a Mac
LANG = C
ACTIVATE_ENV = eval "$$(micromamba shell hook --shell bash)" && micromamba activate $(PROJECT) 
VERSION := $(shell $(ACTIVATE_ENV) && poetry run pato-gui-version)
TAG := v$(VERSION)

.PHONY: clean install test dist distclean upload_test upload tag

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)
#	@echo home: $(home)

env-bootstrap: ## Bootstrap an environment
	micromamba env create --yes --name $(PROJECT) python=$(PYTHON_VERSION)
	micromamba env export --from-history > environment.yml

env-create: ## Create Conda environment (only once)
	micromamba env create --yes --name $(PROJECT) --file environment.yml

env-update: env-remove env-create ## Update Conda environment

env-remove: ## Remove Conda environment
	-micromamba env remove --yes --name $(PROJECT)

init: ## Fulfill the requirements
	$(ACTIVATE_ENV) && poetry build

clean: ## Cleanup the environment
	$(GIT) clean -d -x -i

install: init ## Install the package to the Python installation path.
	$(ACTIVATE_ENV) && poetry install

test: install ## Test the package.
	$(ACTIVATE_ENV) && poetry run pytest

# dist: install test ## Prepare the distribution the package by installing and testing it.

# upload_test: dist ## Upload the package to PyPI test.

# upload: dist ## Upload the package to PyPI.

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"
