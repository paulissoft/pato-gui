## -*- mode: make -*-

# project specific
PROJECT        := pato-gui
BRANCH 	 	     := main
PYTHON_VERSION := 3.12

GIT 			     := git
# Otherwise perl may complain on a Mac
LANG           := C
# Must be invoked dynamic, i.e. the environment may not be ready yet
VERSION         = $(shell poetry version -s)
# Idem
TAG 	          = v$(VERSION)

DOCKER_LOG_LEVEL     := INFO
DOCKER_OPTIONS       := --log-level $(DOCKER_LOG_LEVEL)
DOCKER_IMAGE_NAME    := pato-gui
DOCKER_IMAGE_TAG     := pato-gui
DOCKER_BUILD_OPTIONS := --file .devcontainer/Dockerfile --tag $(DOCKER_IMAGE_TAG)
DOCKER_BUILD_FILE    := .

# Goals not needing a virtual environment
GOALS_ENV_NO   := help env-bootstrap env-create env-update env-remove clean tag docker-build docker-run
# Goals needing a virtual environment (all the poetry commands)
GOALS_ENV_YES  := init install pato-gui pato-gui-build test dist upload_test upload 

ifneq '$(filter $(GOALS_ENV_YES),$(MAKECMDGOALS))' ''

DEVBOX_PROJECT_ROOT ?=

ifeq '$(VIRTUAL_ENV)' ''
$(error Set up virtual environment (source .venv/bin/activate))
endif

endif

.PHONY: $(GOALS_ENV_NO) $(GOALS_ENV_YES)

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

init: ## Fulfill the requirements
	poetry build

clean: ## Cleanup the environment
	$(GIT) clean -d -x -i

install: init ## Install the package to the Python installation path.
	poetry install
	poetry lock

docker-build: ## Build the docker image
	DOCKER_BUILDKIT=1 docker $(DOCKER_OPTIONS) buildx build $(DOCKER_BUILD_OPTIONS) $(DOCKER_BUILD_FILE)

docker-run: docker-build ## Build the docker image
	docker $(DOCKER_OPTIONS) run --it --rm --name $(DOCKER_IMAGE_NAME) $(DOCKER_IMAGE_TAG)

pato-gui: install ## Run the PATO GUI
	poetry run $@

pato-gui-build: install ## Build the PATO GUI exectable
	poetry run $@

test: install ## Test the package.
	poetry check
	poetry run pytest

dist: install test ## Prepare the distribution the package by installing and testing it.

upload_test: dist ## Upload the package to PyPI test.
	poetry publish -r test-pypi

upload: dist ## Upload the package to PyPI.
	poetry publish

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"
