## -*- mode: make -*-

# project specific
PROJECT        := pato-gui
BRANCH 	 	     := main
PYTHON_VERSION := 3.12

POETRY               := poetry
POETRY_OPTIONS       :=
POETRY_CMD           := $(POETRY) $(POETRY_OPTIONS)

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
DOCKER_BUILD_OPTIONS := --tag $(DOCKER_IMAGE_TAG)
DOCKER_BUILD_FILE    := .

# Goals not needing a virtual environment
GOALS_VIRTUAL_ENV_NO   := help tag clean docker-build docker-run
# Goals needing a virtual environment (all the poetry commands)
GOALS_VIRTUAL_ENV_YES  := all init install pato-gui pato-gui-build test dist upload_test upload 

ifneq '$(filter $(GOALS_VIRTUAL_ENV_YES),$(MAKECMDGOALS))' ''

ifeq '$(VIRTUAL_ENV)' ''
$(error Set up virtual environment (source .venv/bin/activate))
endif

endif

.PHONY: $(GOALS_VIRTUAL_ENV_NO) $(GOALS_VIRTUAL_ENV_YES)

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

all: init install pato-gui-build  ## Do it all: initialize, install and build the executable

init: ## Fulfill the requirements
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

clean: ## Cleanup the environment
	$(GIT) clean -d -x -i

docker-build: ## Build the docker image
	DOCKER_BUILDKIT=1 docker $(DOCKER_OPTIONS) buildx build $(DOCKER_BUILD_OPTIONS) $(DOCKER_BUILD_FILE)

docker-run: docker-build ## Build the docker image
	docker $(DOCKER_OPTIONS) run --it --rm --name $(DOCKER_IMAGE_NAME) $(DOCKER_IMAGE_TAG)
