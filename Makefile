## -*- mode: make -*-

# project specific
PROJECT        := pato-gui
BRANCH         := main
PYTHON_VERSION := 3.12
DEVBOX         := devbox
GH             := gh

# Otherwise perl may complain on a Mac on "make help"
LANG           := C

# 1 - always run commands in devshell environment, i.e. devbox run --
ifneq '$(DEVBOX_SHELL_ENABLED)' '1'
DEVBOX_RUN     := $(DEVBOX) run --
else
DEVBOX_RUN     := 
endif

# 2 - always run poetry commands in micromamba environment, i.e. $(DEVBOX_RUN) micromamba -n $(PROJECT) run
MAMBA          := $(DEVBOX_RUN) micromamba
MAMBA_RUN      := $(MAMBA) -n $(PROJECT) run
POETRY         := $(MAMBA_RUN) poetry
GIT            := $(DEVBOX_RUN) git

# Must be invoked dynamic, i.e. the environment may not be ready yet
VERSION         = $(shell $(POETRY) version -s)
# Idem
TAG             = v$(VERSION)

CONDA_DEFAULT_ENV=pato-gui

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
	$(GH) release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"

clean: env-remove ## Cleanup the environment
	$(GIT) clean -d -x -i

.PHONY: help \
        all \
        env-create \
        env-export \
        env-update \
        env-remove \
        init \
        install \
        test \
        dist \
        upload_test \
        upload \
        pato-gui \
        pato-gui-build \
        tag \
        clean

