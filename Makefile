## -*- mode: make -*-

# project specific
PROJECT        := pato-gui
BRANCH 	 	     := main
PYTHON_VERSION := 3.12

MAMBA          := micromamba
GIT 			     := git
# Otherwise perl may complain on a Mac
LANG           := C
# Must be invoked dynamic, i.e. the environment may not be ready yet
POETRY         := $(MAMBA) -n $(PROJECT) run poetry
VERSION         = $(shell $(POETRY) version -s)
# Idem
TAG 	          = v$(VERSION)

DOCKER               := podman
DOCKER_LOG_LEVEL     := INFO
DOCKER_OPTIONS       := --log-level $(DOCKER_LOG_LEVEL)
DOCKER_IMAGE_NAME    := pato-gui
DOCKER_IMAGE_TAG     := pato-gui
PLATFORM             := --platform linux/amd64
DOCKER_BUILD_OPTIONS := $(PLATFORM) --tag $(DOCKER_IMAGE_TAG)
DOCKER_BUILD_FILE    := .

CONDA_DEFAULT_ENV=pato-gui

# Goals not needing a Mamba (Conda) environment
GOALS_ENV_NO   := help env-create env-export env-update env-remove tag clean docker-build docker-run
# Goals needing a Mamba (Conda) environment (all the poetry commands)
GOALS_ENV_YES  := all init install test dist pato-gui pato-gui-build upload_test upload 

#ifneq '$(filter $(GOALS_ENV_YES),$(MAKECMDGOALS))' ''
#
#ifneq '$(CONDA_DEFAULT_ENV)' '$(PROJECT)'
#$(error Set up Conda environment ($(MAMBA) activate $(PROJECT)))
#endif
#
#endif

.PHONY: $(GOALS_ENV_NO) $(GOALS_ENV_YES)

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

all: env-create init install test pato-gui-build

env-create: ## Create Mamba (Conda) environment (only once)
	$(MAMBA) env list | grep -E '^\s*$(PROJECT)\s+' || $(MAMBA) env create --name $(PROJECT) --file environment.yml --yes

env-export: ## Export an environment
	$(MAMBA) create --name $(PROJECT) python
	$(MAMBA) env export --from-history > environment.yml

env-update: ## Update Mamba (Conda) environment
	$(MAMBA) env update --name $(PROJECT) --file environment.yml --prune

env-remove: ## Remove Mamba (Conda) environment
	-$(MAMBA) env remove --name $(PROJECT)

init: env-create ## Fulfill the requirements
	$(POETRY) install

install: init ## Install the package to the Python installation path.
	$(POETRY) lock

test: install ## Test the package.
	$(POETRY) check
	$(POETRY) run pytest

dist: install test ## Prepare the distribution the package by installing and testing it.

upload_test: dist ## Upload the package to PyPI test.
	$(POETRY) publish -r test-pypi

upload: dist ## Upload the package to PyPI.
	$(POETRY) publish

pato-gui-build: install ## Build the PATO GUI exectable
	$(POETRY) run $@

pato-gui: install ## Run the PATO GUI
	$(POETRY) run $@

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"

clean: env-remove ## Cleanup the environment
	$(GIT) clean -d -x -i

docker-build: ## Build the docker image
	$(DOCKER) $(DOCKER_OPTIONS) build $(DOCKER_BUILD_OPTIONS) $(DOCKER_BUILD_FILE)

docker-run: docker-build ## Build the docker image
	$(DOCKER) $(DOCKER_OPTIONS) run -it --platform linux/amd64 --rm --name $(DOCKER_IMAGE_NAME) $(DOCKER_IMAGE_TAG)
