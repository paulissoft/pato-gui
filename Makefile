## -*- mode: make -*-

# project specific
PROJECT        := pato-gui
BRANCH 	 	     := main
PYTHON_VERSION := 3.12
POETRY         := poetry
POETRY_OPTIONS :=
POETRY_CMD     := $(POETRY) $(POETRY_OPTIONS)
MAMBA          := mamba
GIT 			     := git
# Otherwise perl may complain on a Mac
LANG           := C
# Must be invoked dynamic, i.e. the environment may not be ready yet
VERSION         = $(shell $(POETRY_CMD) version -s)
# Idem
TAG 	          = v$(VERSION)

DOCKER_LOG_LEVEL     := INFO
DOCKER_OPTIONS       := --log-level $(DOCKER_LOG_LEVEL)
DOCKER_IMAGE_NAME    := pato-gui
DOCKER_IMAGE_TAG     := pato-gui
DOCKER_BUILD_OPTIONS := --platform linux/amd64 --tag $(DOCKER_IMAGE_TAG)
DOCKER_BUILD_FILE    := .

# Goals not needing a Mamba (Conda) environment
GOALS_VIRTUAL_ENV_NO   := help env-bootstrap env-create env-update env-remove clean tag docker-build docker-run
# Goals needing a Mamba (Conda) environment (all the poetry commands)
GOALS_VIRTUAL_ENV_YES  := init install pato-gui pato-gui-build test dist upload_test upload 

ifneq '$(filter $(GOALS_VIRTUAL_ENV_YES),$(MAKECMDGOALS))' ''

ifneq '$(CONDA_DEFAULT_ENV)' '$(PROJECT)'
$(error Set up Conda environment ($(MAMBA) activate $(PROJECT)))
endif

endif

.PHONY: $(GOALS_VIRTUAL_ENV_NO) $(GOALS_VIRTUAL_ENV_YES)

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

all: init install pato-gui-build  ## Do it all: initialize, install and build the executable

env-bootstrap: ## Bootstrap an environment
	$(MAMBA) create --name $(PROJECT) python
	$(MAMBA) env export --from-history > environment.yml

env-create: ## Create Mamba (Conda) environment (only once)
	$(MAMBA) env create --name $(PROJECT) --file environment.yml

env-update: ## Update Mamba (Conda) environment
	$(MAMBA) env update --name $(PROJECT) --file environment.yml --prune

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

docker-build: ## Build the docker image
	DOCKER_BUILDKIT=1 docker $(DOCKER_OPTIONS) buildx build $(DOCKER_BUILD_OPTIONS) $(DOCKER_BUILD_FILE)

docker-run: docker-build ## Build the docker image
	docker $(DOCKER_OPTIONS) run --it --rm --name $(DOCKER_IMAGE_NAME) $(DOCKER_IMAGE_TAG)
