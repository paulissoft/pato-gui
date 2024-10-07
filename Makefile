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
DOCKER_BUILD_OPTIONS := --tag $(DOCKER_IMAGE_TAG)
DOCKER_BUILD_FILE    := .

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

init: ## Fulfill the requirements
	pixi install
	poetry build

clean: ## Cleanup the environment
	$(GIT) clean -d -x -i

install: init ## Install the package to the Python installation path.
	pixi 

docker-build: ## Build the docker image
	DOCKER_BUILDKIT=1 docker $(DOCKER_OPTIONS) buildx build $(DOCKER_BUILD_OPTIONS) $(DOCKER_BUILD_FILE)

docker-run: docker-build ## Build the docker image
	docker $(DOCKER_OPTIONS) run -it --rm --name $(DOCKER_IMAGE_NAME) $(DOCKER_IMAGE_TAG)

pato-gui: install ## Run the PATO GUI
	pixi run $@

pato-gui-build: install ## Build the PATO GUI exectable
	pixi run $@

test: install ## Test the package.
	pixi run  --environment dev pytest

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"

.PHONY: help init clean install docker-build docker-run pato-gui pato-gui-build test tag
