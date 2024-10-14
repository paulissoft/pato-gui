## -*- mode: make -*-

# project specific
PROJECT        := pato-gui
BRANCH 	 	     := main
PYTHON_VERSION := 3.12
CONDA          := conda
MAMBA          := mamba
POETRY         := poetry
POETRY_OPTIONS :=
POETRY_CMD     := $(CONDA) run -n $(PROJECT) $(POETRY) $(POETRY_OPTIONS)
GIT 			     := git
# Otherwise perl may complain on a Mac
LANG           := C
# Must be invoked dynamic, i.e. the environment may not be ready yet
VERSION         = $(shell $(POETRY_CMD) version -s)
# Idem
TAG 	          = v$(VERSION)

# Goals not needing a Mamba (Conda) environment
GOALS_VIRTUAL_ENV_NO   := help env-create env-update env-export env-remove clean tag
# Goals needing a Mamba (Conda) environment (all the poetry commands)
GOALS_VIRTUAL_ENV_YES  := init install pato-gui pato-gui-build test dist upload_test upload 

#ifneq '$(filter $(GOALS_VIRTUAL_ENV_YES),$(MAKECMDGOALS))' ''
#
#ifneq '$(CONDA_DEFAULT_ENV)' '$(PROJECT)'
#$(error Set up Conda environment ($(MAMBA) activate $(PROJECT)))
#endif
#
#endif

.PHONY: $(GOALS_VIRTUAL_ENV_NO) $(GOALS_VIRTUAL_ENV_YES)

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

all: init install pato-gui-build  ## Do it all: initialize, install and build the executable

#env-bootstrap: ## Bootstrap an environment
#	$(MAMBA) create --yes --name $(PROJECT) python

env-create: ## Create Mamba (Conda) environment (only once)
	$(MAMBA) env list | grep -E '^$(PROJECT)\s' 1>/dev/null || $(MAMBA) env create --name $(PROJECT) --file environment.yml

env-update: ## Update Mamba (Conda) environment
	$(MAMBA) env update --name $(PROJECT) --file environment.yml --prune

env-export: ## Export the the environment to file environment.yml
	$(MAMBA) env export --from-history > environment.yml

env-remove: ## Remove Mamba (Conda) environment
	-$(MAMBA) env remove --name $(PROJECT)

init: env-create ## Fulfill the requirements
	$(POETRY_CMD) build

install: init ## Install the package to the Python installation path.
	$(POETRY_CMD) install
	$(POETRY_CMD) lock

pato-gui: install ## Run the PATO GUI
	$(POETRY_CMD) run $@

pato-gui-build: install ## Build the PATO GUI exectable
	$(POETRY_CMD) run $@

test: install ## Test the package.
	$(POETRY_CMD) check
	$(POETRY_CMD) run pytest

dist: install test ## Prepare the distribution the package by installing and testing it.

upload_test: dist ## Upload the package to PyPI test.
	$(POETRY_CMD) publish -r test-pypi

upload: dist ## Upload the package to PyPI.
	$(POETRY_CMD) publish

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"

clean: env-remove ## Cleanup the environment
	$(GIT) clean -d -x -i
