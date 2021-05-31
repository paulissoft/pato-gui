# Oracle Tools GUI Makefile

# Just a snippet to stop executing under other make(1) commands
# that won't understand these lines
ifneq (,)
This makefile requires GNU Make.
endif

# Disable built-in rules and variables plus clean the suffix rules
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.SUFFIXES:

# OS specific section (see https://stackoverflow.com/questions/714100/os-detecting-makefile/52062069#52062069)
ifeq '$(findstring ;,$(PATH))' ';'
    detected_OS := Windows
else
    detected_OS := $(shell uname 2>/dev/null || echo Unknown)
    detected_OS := $(patsubst CYGWIN%,Cygwin,$(detected_OS))
    detected_OS := $(patsubst MSYS%,MSYS,$(detected_OS))
    detected_OS := $(patsubst MINGW%,MSYS,$(detected_OS))
endif

ifeq ($(detected_OS),Windows)
    CAT := type
    RM_F := del /q
    RM_FR := rmdir /q/s
    NOWHERE := nul
else
    CAT := cat
    RM_F := rm -f
    RM_FR := rm -fr
    NOWHERE := /dev/null
endif

PYINSTALLER_OPTIONS := --clean --noconfirm

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^([a-zA-Z_-]+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

spec: oracle-tools-gui.spec ## Build specification.

oracle-tools-gui.spec: oracle-tools-gui.py
	pyinstaller $(PYINSTALLER_OPTIONS) $?

dist: oracle-tools-gui.spec ## Build distribution.
	pyinstaller $(PYINSTALLER_OPTIONS) $?

clean: ## Cleanup output files.
	-$(RM_FR) build __pycache__ 2>$(NOWHERE)

distclean: clean ## Runs clean first and then cleans up dependency include files. 
	-$(RM_FR) dist 2>$(NOWHERE)

.PHONY: help spec dist clean distclean
