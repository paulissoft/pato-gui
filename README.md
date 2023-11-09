# pato-gui

## Table of contents

1. [Introduction](#introduction)
2. [Installation](#installation)
   1. [Start a command prompt](#start-command-line-prompt)
   2. [Installing from source](#installing-from-source)
   3. [Installing from PyPi](#installing-from-pypi)
3. [Usage](#usage)
   1. [Launch the GUI](#launch-the-gui)
   2. [Help](#help)
4. [Links](#links)

## Introduction <a name="introduction" />

A Python GUI for [PATO](https://github.com/paulissoft/oracle-tools) as an alternative for the Maven command line.

First you probably need to clone PATO so you use its Maven POM files or other Maven POM files having them as parent.

This GUI would not have been possible without [Gooey](https://github.com/chriskiehl/Gooey).

## Installation <a name="installation" />

This utility needs Python 3. In order to support several Python versions/environments on your computer, I prefer [Mamba from the Miniforge project on GitHub](https://github.com/conda-forge/miniforge). See the installation instructions there if you want to use that distribution. Mamba is an environment manager similar to Conda variants like Anaconda and [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html) but much faster. Together with [Poetry](https://python-poetry.org/docs/) this is a good combination to distribute libraries to PyPi.

### Start a command prompt <a name="start-command-line-prompt" />

Needed for installing and running the PATO GUI. Please Google it if you don't know how to start a command prompt.

First please note that the dollar sign you will see below is the command line prompt sign and not a character you have to type.
The command line prompt will differ between Operating Systems.

### Installing from source <a name="installing-from-source" />

Clone the Git repo [pato-gui](https://github.com/paulissoft/pato-gui) first.

Go to the root folder and issue this command for more help:

```
$ make help
```

To run from the start:

```
$ make env-create
$ mambo activate pato-gui
$ make test
$ make run
```

### Installing from PyPi <a name="installing-from-pypi" />

```
$ python3 -m pip install pato-gui
```

Now `pato-gui` should be available and this command shows you the help:

```
$ pato-gui -h
```

You can also build an executable and put it somewhere in your path:

```
$ pato-gui-build
```

In the `dist/PatoGui` folder you will find the `PatoGui` executable.

## Usage <a name="usage" />

### Launch the GUI <a name="launch-the-gui" />

This:

```
$ make run
```

or using the executable this:

```
$ <path to PatoGui>/PatoGui
```

A graphical interface will pop up.

If you know the Maven POM file already:

```
$ python3 <pato-gui root>/src/pato_gui/pato-gui.py <POM file>
```

or:

```
$ <path to PatoGui>/PatoGui <POM file>
```

### Help <a name="help" />

From the command line:

```
$ python3 <pato-gui root>/src/pato_gui/pato-gui.py -h
```

or:

```
$ <path to PatoGui>/PatoGui -h
```

And in the left top corner of the GUI screen there is a Help button.

## Links <a name="links" />

- [using python-poetry to publish to test.pypi.org](https://stackoverflow.com/questions/68882603/using-python-poetry-to-publish-to-test-pypi-org)

### Migrate to Poetry

- [Poetry Read The Docs](https://python-poetry.org/docs/)
- [Migrating a project to Poetry](https://browniebroke.com/blog/migrating-project-to-poetry/)
- [Convert Python requirements to Poetry format](https://browniebroke.com/blog/convert-requirements-to-pyproject/)
- [Specify docs dependency groups with Poetry and Read the Docs](https://browniebroke.com/blog/specify-docs-dependency-groups-with-poetry-and-read-the-docs/)
- [Convert a Poetry package to the src layout](https://browniebroke.com/blog/convert-existing-poetry-to-src-layout/)
- [Use poetry to create binary distributable with pyinstaller on package?](https://stackoverflow.com/questions/76145761/use-poetry-to-create-binary-distributable-with-pyinstaller-on-package)
- [Setup Guide for Poetry Dev Environment on Apple Silicon.](https://github.com/rybodiddly/Poetry-Pyenv-Homebrew-Numpy-TensorFlow-on-Apple-Silicon-M1)
- [https://stackoverflow.com/questions/70851048/does-it-make-sense-to-use-conda-poetry](https://stackoverflow.com/questions/70851048/does-it-make-sense-to-use-conda-poetry)
- [Conda and Poetry: A Harmonious Fusion](https://medium.com/@silvinohenriqueteixeiramalta/conda-and-poetry-a-harmonious-fusion-8116895b6380#:~:text=Conda%20and%20Poetry%20are%20two,dependency%20resolution%2C%20and%20package%20distribution.)
- [Welcome to Mamba’s documentation!](https://mamba.readthedocs.io/en/latest/index.html)
- [How to Use Poetry with Conda for Package Management on a Specific Python Version](https://michhar.github.io/2023-07-poetry-with-conda/)
- [Examples of using conda + poetry for cross-platform Python package portability](https://shandou.medium.com/examples-of-using-conda-poetry-for-cross-platform-python-package-portability-711a7450a522)
- [Mambaforge/miniforge](https://github.com/conda-forge/miniforge)
