## -*- mode: make -*-

# project specific
PROJECT    := pato-gui
BRANCH 	   := main
VERSION_PY := src/pato_gui/app.py

# PYTHON is determined later so use = and not :=
VERSION     = $(shell $(PYTHON) $(VERSION_PY) __version__)

GIT = git
# least important first (can not stop easily in foreach)
PYTHON_EXECUTABLES = python python3 

# Otherwise perl may complain on a Mac
LANG = C
# This is GNU specific I guess
TAG = v$(VERSION)

# OS specific section
ifeq '$(findstring ;,$(PATH))' ';'
detected_OS := Windows
GREP        := find
else
detected_OS := $(shell uname 2>/dev/null || echo Unknown)
detected_OS := $(patsubst CYGWIN%,Cygwin,$(detected_OS))
detected_OS := $(patsubst MSYS%,MSYS,$(detected_OS))
detected_OS := $(patsubst MINGW%,MSYS,$(detected_OS))
GREP        := grep
endif

ifdef CONDA_PYTHON_EXE
$(error Can not use a conda (Miniconda or Anaconda) environment: please use a default Python distribution)
else
PYTHON := $(shell perl -MFile::Which -e 'foreach (@ARGV) { if (which($$_)) { print; exit 0; } }' $(PYTHON_EXECUTABLES))
endif

ifndef PYTHON
$(error Could not find any Python executable from ${PYTHON_EXECUTABLES}.)
endif

.PHONY: help init clean test dist tag

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)
#	@echo home: $(home)

init: ## Just install the requirements
	python3 -m pip install --upgrade --quiet briefcase
	briefcase dev --no-run

clean: ## Cleanup the package and remove it from the Python installation path.
	git clean -d -x -f -i

run: init ## Run the package from source.
	briefcase dev

test: init ## Test the package.
	briefcase dev --test

dist: test ## Prepare the distribution package by building, testing and running it.
	briefcase create --no-input
	briefcase build -u -r
	briefcase package --adhoc-sign

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)

upload: ## Upload the package to GitHub.
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"
	-find dist -name pato-gui-$(VERSION).dmg -exec gh release upload $(TAG) {} --clobber \;
