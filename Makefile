## -*- mode: make -*-

GIT = git
PYTHON = python
MYPY = mypy
PIP = $(PYTHON) -m pip
PROJECT = oracle-tools-gui
# Otherwise perl may complain on a Mac
LANG = C

# OS specific section
ifeq '$(findstring ;,$(PATH))' ';'
    detected_OS := Windows
else
    detected_OS := $(shell uname 2>/dev/null || echo Unknown)
    detected_OS := $(patsubst CYGWIN%,Cygwin,$(detected_OS))
    detected_OS := $(patsubst MSYS%,MSYS,$(detected_OS))
    detected_OS := $(patsubst MINGW%,MSYS,$(detected_OS))
endif

ifeq ($(detected_OS),Windows)
    SHELL = cmd
    RM_EGGS = pushd $(CONDA_PREFIX) && del /s/p $(PROJECT).egg-link $(PROJECT)-nspkg.pth
else
    RM_EGGS = cd $(CONDA_PREFIX) && find . \( -name $(PROJECT).egg-link -o -name $(PROJECT)-nspkg.pth \) -exec rm -i {} \;
endif

.PHONY: clean install test mypy pytest dist distclean tag

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^([a-zA-Z_-]+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

clean: ## Cleanup output files.
	$(PYTHON) setup.py clean --all
	$(RM_EGGS)
	$(PYTHON) -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	$(PYTHON) -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
	$(PYTHON) -Bc "import shutil; import os; [shutil.rmtree(d) for d in ['.pytest_cache', '.mypy_cache', 'dist', 'htmlcov', '.coverage'] if os.path.isdir(d)]"
	cd src && $(MAKE) clean

install: clean ## Install the Python (test) requirements.
	$(PIP) install -r requirements.txt
	$(PIP) install -r test_requirements.txt
	$(PYTHON) setup.py install

test: mypy pytest ## Test the software.

mypy: ## Run mypy
	$(MYPY) --show-error-codes src

pytest: ## Run pytest
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
