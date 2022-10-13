# oracle-tools-gui

A Python GUI for [Oracle tools](https://github.com/paulissoft/oracle-tools) as an alternative for the Maven command line.

First you probably need to clone Oracle tools so you use its POM files or other POM files having them as parent.

# Installation

This utility needs Python 3. You can install it using the Microsoft Store
(accessible via the Windows 10 start button) or just Google `download Python 3`.

## Start a command prompt

Please Google it if you don't know how.

## Install required Python libraries

Go to the src folder and install them from the command line using pip (or pip3 when `pip --version` displays the Python 2 version):

```
$ cd src
$ pip install -r requirements.txt
```

First please note that the dollar sign is the prompt sign and not a character you have to type.
Next, please do move into src first, since the root also contains a (different) `requirements.txt`.

You may need to use pip3 instead of pip if pip does not point to a Python 3 installation.

# Usage

## Launch the Python script src/oracle_tools_gui.py

This can be done directory from a command prompt or by creating a (Windows)
shortcut on your Desktop (right mouse click, choose New) or an alias on Unix/Mac OS X.

Using the command prompt:

```
$ cd src
$ python oracle_tools_gui.py
```

Please note that you may need to use python3 when `python --version` displays the Python 2 version.

## Help

In the left top corner of the GUI screen there is a Help button.
