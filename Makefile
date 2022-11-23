## -*- mode: make -*-

GIT = git
PYTHON = python
MYPY = mypy
PIP = $(PYTHON) -m pip
PROJECT = pato
# Otherwise perl may complain on a Mac
LANG = C

# OS specific section
ifeq '$(findstring ;,$(PATH))' ';'
    detected_OS := Windows
    HOME = $(USERPROFILE)
else
    detected_OS := $(shell uname 2>/dev/null || echo Unknown)
    detected_OS := $(patsubst CYGWIN%,Cygwin,$(detected_OS))
    detected_OS := $(patsubst MSYS%,MSYS,$(detected_OS))
    detected_OS := $(patsubst MINGW%,MSYS,$(detected_OS))
endif

ifdef CONDA_PREFIX
    home = $(CONDA_PREFIX)
else
    home = $(HOME)
endif

ifeq ($(detected_OS),Windows)
    RM_EGGS = pushd $(home) && del /s/q $(PROJECT).egg-link $(PROJECT)-nspkg.pth
else
    RM_EGGS = { cd $(home) && find . \( -name $(PROJECT).egg-link -o -name $(PROJECT)-nspkg.pth \) -print -exec rm -i "{}" \; ; }
endif

.PHONY: clean install test test dist distclean tag

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^([a-zA-Z_-]+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

clean: ## Cleanup the package and remove it from the Python installation path.
	$(PYTHON) setup.py clean --all
	-$(RM_EGGS)
	$(PYTHON) -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	$(PYTHON) -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
	$(PYTHON) -Bc "import shutil; import os; [shutil.rmtree(d) for d in ['.pytest_cache', '.mypy_cache', 'dist', 'htmlcov', '.coverage'] if os.path.isdir(d)]"
	cd src && $(MAKE) clean

install: ## Install the package to the Python installation path.
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

test: ## Test the package.
	$(PIP) install -r test_requirements.txt
	$(MYPY) --show-error-codes src
	$(PYTHON) -m pytest --exitfirst

dist: install test ## Build distribution.
	cd src && $(MAKE) dist

distclean: ## Runs clean first and then cleans up dependency include files. 
	cd src && $(MAKE) distclean

# This is GNU specific I guess
VERSION = $(shell $(PYTHON) src/utils/about.py)

TAG = v$(VERSION)

BRANCH = main

tag:
	$(GIT) tag -a $(TAG) -m "$(TAG)"
	$(GIT) push origin $(TAG)
	gh release create $(TAG) --target $(BRANCH) --title "Release $(TAG)" --notes "See CHANGELOG"
