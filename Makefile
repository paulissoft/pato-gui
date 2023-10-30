## -*- mode: make -*-

# project specific
PROJECT  := pato-gui
ABOUT_PY := src/pato_gui/about.py
BRANCH 	 := main

GIT = git
# least important first (can not stop easily in foreach)
PYTHON_EXECUTABLES = python python3 

# Otherwise perl may complain on a Mac
LANG = C
# This is GNU specific I guess
VERSION = $(shell $(PYTHON) $(ABOUT_PY))
TAG = v$(VERSION)

# OS specific section
ifeq '$(findstring ;,$(PATH))' ';'
detected_OS := Windows
else
detected_OS := $(shell uname 2>/dev/null || echo Unknown)
detected_OS := $(patsubst CYGWIN%,Cygwin,$(detected_OS))
detected_OS := $(patsubst MSYS%,MSYS,$(detected_OS))
detected_OS := $(patsubst MINGW%,MSYS,$(detected_OS))
endif

ifdef CONDA_PYTHON_EXE
# look no further
PYTHON := $(subst \,/,$(CONDA_PYTHON_EXE))
else
# On Windows those executables may exist but not functional yet (can be used to install) so use Python -V
$(foreach e,$(PYTHON_EXECUTABLES),$(if $(shell ${e}${EXE} -V),$(eval PYTHON := ${e}${EXE}),))
endif

ifndef PYTHON
$(error Could not find any Python executable from ${PYTHON_EXECUTABLES}.)
endif

.PHONY: help init clean test dist tag

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)
#	@echo home: $(home)

init: ## Just install the requirements
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
	briefcase run --test
	briefcase run
	briefcase package --adhoc-sign

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"
	find . -name pato-gui.app -exec gh release upload $(TAG) {} --clobber \;
