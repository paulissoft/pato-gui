## -*- mode: make -*-

# project specific
PROJECT        := pato-gui
BRANCH 	 	     := main
PYTHON_VERSION := 3.12

MAMBA          := mamba
GIT 			     := git
# Otherwise perl may complain on a Mac
LANG           := C
# Must be invoked dynamic, i.e. the environment may not be ready yet
VERSION         = $(shell poetry run pato-gui-version)
# Idem
TAG 	          = v$(VERSION)

gpaulissen@macmini2020 pato-gui % conda activate pato-gui
(pato-gui) gpaulissen@macmini2020 pato-gui % set | grep CONDA       
CONDA_DEFAULT_ENV=pato-gui

.PHONY: help env-bootstrap env-create env-update env-remove init clean install run test dist upload_test upload tag

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

env-bootstrap: ## Bootstrap an environment
	$(MAMBA) env create --name $(PROJECT) python=$(PYTHON_VERSION)
	$(MAMBA) env export --from-history > environment.yml

env-create: ## Create Conda environment (only once)
	$(MAMBA) env create --name $(PROJECT) --file environment.yml

env-update: env-remove env-create ## Update Conda environment

env-remove: ## Remove Conda environment
	-$(MAMBA) env remove --name $(PROJECT)

init: ## Fulfill the requirements
	poetry build

clean: ## Cleanup the environment
	$(GIT) clean -d -x -i

install: init ## Install the package to the Python installation path.
	poetry install

run: install ## Run the PATO GUI
	poetry run pato-gui

test: install ## Test the package.
	poetry run pytest

# dist: install test ## Prepare the distribution the package by installing and testing it.

# upload_test: dist ## Upload the package to PyPI test.

# upload: dist ## Upload the package to PyPI.

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"
