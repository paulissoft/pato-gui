## -*- mode: make -*-

# project specific
PROJECT        := pato-gui
BRANCH 	 	     := main
PYTHON_VERSION := 3.12

GIT 			     := git
# Otherwise perl may complain on a Mac
LANG           := C
# Must be invoked dynamic, i.e. the environment may not be ready yet
PIXI           := pixi
POETRY         := $(PIXI) exec poetry
VERSION         = $(shell $(POETRY) version -s)
# Idem
TAG 	          = v$(VERSION)

DOCKER_LOG_LEVEL     := INFO
DOCKER_OPTIONS       := --log-level $(DOCKER_LOG_LEVEL)
DOCKER_IMAGE_NAME    := pato-gui
DOCKER_IMAGE_TAG     := pato-gui
PLATFORM             := --platform linux/amd64
DOCKER_BUILD_OPTIONS := $(PLATFORM) --tag $(DOCKER_IMAGE_TAG)
DOCKER_BUILD_FILE    := .

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

all: init install test pato-gui-build

init: ## Fulfill the requirements
	$(PIXI) install
	$(POETRY) build

install: init ## Install the package to the Python installation path.
	$(POETRY) install
	$(POETRY) lock

test: install ## Test the package.
	$(POETRY) check
	$(POETRY) run pytest

pato-gui-build: install ## Build the PATO GUI exectable
	$(POETRY) run $@

pato-gui: install ## Run the PATO GUI
	$(POETRY) run $@

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"

clean: ## Cleanup the environment
	$(GIT) clean -d -x -i

docker-build: ## Build the docker image
	DOCKER_BUILDKIT=1 docker $(DOCKER_OPTIONS) buildx build $(DOCKER_BUILD_OPTIONS) $(DOCKER_BUILD_FILE)

docker-run: docker-build ## Build the docker image
	docker $(DOCKER_OPTIONS) run -it --rm --name $(DOCKER_IMAGE_NAME) $(DOCKER_IMAGE_TAG)

.PHONY: help all init install test pato-gui-build pato-gui tag clean docker-build docker-run

