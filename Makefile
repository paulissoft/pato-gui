## -*- mode: make -*-

# project specific
PROJECT  := pato-gui
ABOUT_PY := src/utils/about.py
BRANCH 	 := main
PYTHON_VERSION := 3.12

GIT = git
# least important first (can not stop easily in foreach)
PYTHON_EXECUTABLES = python python3 
MYPY = mypy
# The -O flag is used to suppress error messages related to eggs.
# See also https://stackoverflow.com/questions/43177200/assertionerror-egg-link-does-not-match-installed-location-of-reviewboard-at.
VERBOSE := 
PIP = $(PYTHON) -O -m pip $(VERBOSE)
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

ifdef CONDA_EXE
home = $(CONDA_EXE)\..\..  # C:\Users\gjpau\miniconda3\Scripts\conda.exe => C:/Users/gjpau/miniconda3/
else
home = $(HOME)
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

ifeq ($(detected_OS),Windows)
HOME    := $(USERPROFILE)
DEVNUL  := NUL
WHICH   := where
GREP    := find
EXE     := .exe
SHELL   := cmd
RM_EGGS := pushd $(home) && del /s/p $(PROJECT).egg-link $(PROJECT)-nspkg.pth $(PROJECT)$(EXE) $(PROJECT)-script.py*
else
DEVNUL  := /dev/null
WHICH   := which
GREP    := grep
EXE     := 
RM_EGGS := cd $(home) && find . \( -name $(PROJECT).egg-link -o -name $(PROJECT)-nspkg.pth -o -name $(PROJECT)$(EXE) -o -name $(PROJECT)-script.py* \) -exec rm -i {} \;
endif


.PHONY: clean install test dist distclean upload_test upload tag

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^((?:\w|[.%-])+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)
#	@echo home: $(home)

env-bootstrap: ## Bootstrap an environment
	micromamba env create --yes --name $(PROJECT) python=$(PYTHON_VERSION)
	micromamba env export --from-history > environment.yml

env-create: ## Create Conda environment (only once)
	micromamba env create --yes --name $(PROJECT) --file environment.yml

env-update: env-remove env-create ## Update Conda environment

env-remove: ## Remove Conda environment
	-micromamba env remove --yes --name $(PROJECT)

init: ## Fulfill the requirements
	$(PIP) install -r development_requirements.txt -r src/program/requirements.txt

clean: init ## Cleanup the package and remove it from the Python installation path.
	$(PYTHON) setup.py clean --all
	$(RM_EGGS)
	$(PYTHON) -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	$(PYTHON) -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
	$(PYTHON) -Bc "import shutil; import os; [shutil.rmtree(d) for d in ['.pytest_cache', '.mypy_cache', 'dist', 'htmlcov', '.coverage'] if os.path.isdir(d)]"
	cd src && cd program && $(MAKE) clean

install: init ## Install the package to the Python installation path.
	$(PIP) install -e .

test: ## Test the package.
	$(PIP) install -r test_requirements.txt
	$(MYPY) --show-error-codes src
	$(PYTHON) -m pytest --exitfirst

dist: install test ## Prepare the distribution the package by installing and testing it.
	$(PYTHON) setup.py sdist bdist_wheel
	$(PYTHON) -m twine check dist/*
	cd src && cd program && $(MAKE) dist

distclean: clean ## Runs clean first and then cleans up dependency include files. 
	cd src && cd program && $(MAKE) distclean

upload_test: dist ## Upload the package to PyPI test.
	$(PYTHON) -m twine upload -r pypitest dist/*

upload: dist ## Upload the package to PyPI.
	$(PYTHON) -m twine upload -r pypi dist/*

tag: ## Tag the package on GitHub.
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"
