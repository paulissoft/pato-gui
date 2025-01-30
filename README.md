# pato-gui

## Table of contents

1. [Introduction](#introduction)
2. [Installation](#installation)
   1. [Start a command prompt](#start-command-line-prompt)
   2. [Installing from source](#installing-from-source)
3. [Usage](#usage)
   1. [Launch the GUI](#launch-the-gui)
   2. [Help](#help)
4. [Links](#links)

## Introduction <a name="introduction" />

A Python GUI for [PATO](https://github.com/paulissoft/oracle-tools) as an alternative for the Maven command line.

First you probably need to clone PATO so you use its Maven POM files or other Maven POM files having them as parent.

This GUI would not have been possible without [Gooey](https://github.com/chriskiehl/Gooey).

## Installation <a name="installation" />

This utility needs Python 3. In order to support several Python versions and/or (virtual) environments on your computer, I prefer [Devbox from Jetify](https://www.jetify.com/devbox/docs/) as the environment manager for O/S tools like Python. See the installation instructions there. Together with [Poetry](https://python-poetry.org/docs/), a Python package manager, this is a good combination to distribute libraries to PyPi.

Here `devbox` is used to install in the project folder (see `devbox.json`):
- ps
- micromamba
- meson

From there on they will install Python, Poetry and so on but the details are hidden by using `make`.

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

First install the program:

```
$ devbox shell
$ make install
```

or:

```
$ devbox run -- make install
```

During the build you may see `complete: command not found` but that is not a problem.

Now create an alias (put it in your Shell resource file like `~/.bashrc` or `~/.zshrc` to make it permanent):

```
$ alias pato-gui='sdk use java 17.0.9-sem && conda run -n pato-gui pato-gui'
```

This assumes that you have installed globally:
- The `sdk` utility (`brew install sdk`)
- Java version 17.0.9-sem (`sdk install java 17.0.9-sem`)
- Conda derivates like Miniconda (program `conda`), Mamba (`mamba`) or MicroMamba (`micromamba`)

The latter program(s) use an environment for various tools and their versions. Here that environment is `pato-gui`, created during `make install`.

## Usage <a name="usage" />

### Launch the GUI <a name="launch-the-gui" />

I assume that you have the alias `pato-gui` as described above, launch it via:

```
$ pato-gui
```

A graphical interface will pop up.

If you know the Maven POM file already:

```
$ pato-gui <POM file>
```

### Help <a name="help" />

From the command line:

```
$ pato-gui -h
```

And in the left top corner of the GUI screen there is a Help button.

## Links <a name="links" />

These links have been helpful to convert a setuptools based project to Poetry.

- [using python-poetry to publish to test.pypi.org](https://stackoverflow.com/questions/68882603/using-python-poetry-to-publish-to-test-pypi-org)
- [Poetry Read The Docs](https://python-poetry.org/docs/)
- [Migrating a project to Poetry](https://browniebroke.com/blog/migrating-project-to-poetry/)
- [Convert Python requirements to Poetry format](https://browniebroke.com/blog/convert-requirements-to-pyproject/)
- [Specify docs dependency groups with Poetry and Read the Docs](https://browniebroke.com/blog/specify-docs-dependency-groups-with-poetry-and-read-the-docs/)
- [Convert a Poetry package to the src layout](https://browniebroke.com/blog/convert-existing-poetry-to-src-layout/)
- [Use poetry to create binary distributable with pyinstaller on package?](https://stackoverflow.com/questions/76145761/use-poetry-to-create-binary-distributable-with-pyinstaller-on-package)
