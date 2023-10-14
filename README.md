# pato-gui

## Table of contents

1. [Introduction](#introduction)
2. [Installation](#installation)
   1. [Start a command prompt](#start-command-line-prompt)
   2. [Installing the binary Python package](#installing-from-binary-package)
   3. [Installing from source](#installing-from-source)
3. [Usage](#usage)
   1. [Launch the GUI](#launch-the-gui)
   2. [Help](#help)

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

### Installing the binary Python package <a name="installing-from-binary-package" />

```
$ python3 -m pip install pato-gui
```

Now `pato-gui` should be available and this command shows you the help:

```
$ pato-gui -h
```

Output:

```
usage: pato-gui [-h] [-d] [--db-config-dir DB_CONFIG_DIR] [file]

Setup logging

positional arguments:
  file                  The POM file

options:
  -h, --help            show this help message and exit
  -d                    Enable debugging
  --db-config-dir DB_CONFIG_DIR
                        The database configuration directory
```

### Installing from source <a name="installing-from-source" />

Only for die-hards having GNU `make` (usually available on Unix). Clone the Git repo [pato-gui](https://github.com/paulissoft/pato-gui) first.

Go to the root folder and issue:

```
$ make install
```

For help:

```
$ make help
```

## Usage <a name="usage" />

### Launch the GUI <a name="launch-the-gui" />

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
