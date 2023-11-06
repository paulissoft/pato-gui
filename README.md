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

This utility needs Python 3. You can install it using the Microsoft Store
(accessible via the Windows start button) or just Google `download Python 3`.

A Python alternative that is more cross-platform is
[Miniconda](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html),
that allows you to switch between several Python environments.

### Start a command prompt <a name="start-command-line-prompt" />

Needed for installating and running the PATO GUI. Please Google it if you don't know how.

First please note that the dollar sign you will see below is the command line prompt sign and not a character you have to type.
The command line prompt will differ between Operating Systems.

### Installing from source <a name="installing-from-source" />

Clone the Git repo [pato-gui](https://github.com/paulissoft/pato-gui) first.

Go to the root folder and issue:

```
$ python3 -O -m pip install -r src/program/requirements.txt
$ python3 -O -m pip install -e .
```

You may need to use `python`instead of `python3`

<!-- 

### Installing the binary Python package <a name="installing-from-binary-package" />

```
$ python3 -m pip install pato-gui
```

Now `pato-gui` should be available and this command shows you the help:

```
$ pato-gui -h
```

-->

## Usage <a name="usage" />

### Launch the GUI <a name="launch-the-gui" />

```
$ python3 <pato-gui root>/src/program/pato_gui.py
```

A graphical interface will pop up.

If you know the Maven POM file already:

```
$ python3 <pato-gui root>/src/program/pato_gui.py <POM file>
```

### Help <a name="help" />

From the command line:

```
$ python3 <pato-gui root>/src/program/pato_gui.py -h
```

And in the left top corner of the GUI screen there is a Help button.

## Links <a name="links" />

- [using python-poetry to publish to test.pypi.org](https://stackoverflow.com/questions/68882603/using-python-poetry-to-publish-to-test-pypi-org)

### Migrate to Poetry

- [Migrating a project to Poetry](https://browniebroke.com/blog/migrating-project-to-poetry/)
- [Convert Python requirements to Poetry format](https://browniebroke.com/blog/convert-requirements-to-pyproject/)
- [Specify docs dependency groups with Poetry and Read the Docs](https://browniebroke.com/blog/specify-docs-dependency-groups-with-poetry-and-read-the-docs/)
- [Convert a Poetry package to the src layout](https://browniebroke.com/blog/convert-existing-poetry-to-src-layout/)
- [Use poetry to create binary distributable with pyinstaller on package?](https://stackoverflow.com/questions/76145761/use-poetry-to-create-binary-distributable-with-pyinstaller-on-package)
