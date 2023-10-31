# PATO GUI

## Table of contents

1. [Introduction](#introduction)
2. [Programs needed](#programs)
   1. [Start a command prompt for verification](#start-command-line-prompt)
   2. [Always needed](#always-needed)
      1. [Python](#python)
      2. [Perl](#perl)
   3. [Launch program via the command line only](#command-line-only)
      1. [Git](#git)
      2. [Make](#make)
   4. [Launch program as an O/S application](#os-application)
      1. [Maven](#maven)
      2. [Java](#java)
      3. [Sql client](#sqlcl)
3. [Installation](#installation)
   1. [Installing from source](#installing-from-source)
   2. [Installing the binary package](#installing-binary-package)
4. [Usage](#usage)
   1. [Launch the GUI](#launch-the-gui)
   2. [Problems](#problems)
   3. [Help](#help)
   4. [Examples](#examples)

## Introduction <a name="introduction" />

A Python GUI for [PATO](https://github.com/paulissoft/oracle-tools) as an alternative for the Maven command line.

This GUI would not have been possible without [Gooey](https://github.com/chriskiehl/Gooey).

## Programs needed <a name="programs" />

Some of the programs will not be needed if you download the binary package from the [releases](https://github.com/paulissoft/pato-gui/releases).

### Start a command prompt for verification <a name="start-command-line-prompt" />

Needed for checking whether programs are available and running the GUI later on.

NOTE: Every time you change the O/S environment (variables like PATH and so on) you will need to restart the command prompt before the changes will be effective.

First please note that the dollar sign you will see below is the command line prompt sign and not a character you have to type.
The command line prompt will differ between Operating Systems.

An example:

```
$ echo Hello World
```

### Always needed <a name="always-needed" />

#### Python <a name="python" />

This utility needs Python 3. 

On Windows you can install Python using the Microsoft Store
(accessible via the Windows start button) or just Google `download Python 3`.

On a Mac it should be installed already as `/usr/bin/python3`.

NOTE: do NOT use a Python alternative like 
[Miniconda](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html).
This is because the PATO GUI will be installed into the Applications folder
meaning the user environment will be stripped down to the minimum when the
application is started, i.e. without Miniconda. Hence there is mismatch between
the development and run-time environment.

Check that Python has a version at least 3.6:

```
$ python3 -V
```

Output something like:

```
Python 3.10.9
```

#### Perl <a name="perl" />

You need at least 5.16.3.

Check:

```
$ perl -v
```

Output like:

```
This is perl 5, version 30, subversion 3 (v5.30.3) built for darwin-thread-multi-2level
(with 2 registered patches, see perl -V for more detail)

Copyright 1987-2020, Larry Wall

Perl may be copied only under the terms of either the Artistic License or the
GNU General Public License, which may be found in the Perl 5 source kit.

Complete documentation for Perl, including FAQ lists, should be found on
this system using "man perl" or "perldoc perl".  If you have access to the
Internet, point your browser at http://www.perl.org/, the Perl Home Page.
```

### Launch program via the command line only <a name="command-line-only" />

#### Git <a name="git" />

Git (the executable is named `git`) will usually be available on a Unix system (like Linux or a Mac).
The GitHub Desktop program (any platform) is easy to use and install (use Google with "download GitHub Desktop").

Check:

```
$ git -v
```

Output something like:

```
git version 2.39.3 (Apple Git-145)
```

#### Make <a name="make" />

You need the GNU variant of Make.
Make is usually available on any Unix system. 
For Windows you can use [Chocolatey](https://chocolatey.org) to install it.

Check:

```
$ make -v
```

Output is something like:

```
GNU Make 3.81
Copyright (C) 2006  Free Software Foundation, Inc.
This is free software; see the source for copying conditions.
There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.
```

### Launch program as an O/S application <a name="os-application" />

For a Mac this means an application installed from a `.dmg` file into `/Applications`.

For Windows this means an application installed via a `.msi` file.

For Linux this is an `.AppImage` file.

#### Maven <a name="maven" />

Use Google to download and install it (on a Mac you can use `brew`). You need at least version 3.6.

Check:

```
$ mvn -v
```

Output like:

```
Apache Maven 3.8.7 (b89d5959fcde851dcb1c8946a785a163f14e1e29)
Maven home: /usr/local/Cellar/maven/3.8.7/libexec
Java version: 19.0.2, vendor: Homebrew, runtime: /usr/local/Cellar/openjdk/19.0.2/libexec/openjdk.jdk/Contents/Home
Default locale: en_FR, platform encoding: UTF-8
OS name: "mac os x", version: "14.0", arch: "x86_64", family: "mac"
```

#### Java <a name="java" />

You need the JDK variant with a version at least 11.

Check:

```
$ javac -version
```

Output like:

```
javac 11.0.10
```

#### Sql client <a name="sqlcl" />

You can download the SQL client "SQLcl" from Oracle. You can download the [latest SQLCL zip here](https://download.oracle.com/otn_software/java/sqldeveloper/sqlcl-latest.zip).

Next install it in a global directory, something like `/opt/oracle/sqlcl`. 

On Unix you need root privileges so use `sudo`:

```
$ sudo mkdir -p /opt/oracle
$ sudo cd /opt/oracle
$ # sudo wget https://download.oracle.com/otn_software/java/sqldeveloper/sqlcl-latest.zip
$ sudo unzip /path/to/sqlcl-latest.zip
```

Now `/opt/oracle/sqlcl/bin` needs to be added to your PATH.

## Installation <a name="installation" />

### Installing from source <a name="installing-from-source" />

Start a command line prompt first.

Clone the Git repo [pato-gui](https://github.com/paulissoft/pato-gui) first.

Go to the root folder and issue:

```
$ make help
```

Output will be:

```
help                            This help.
init                            Just install the requirements
clean                           Cleanup the package and remove it from the Python installation path.
run                             Run the package from source.
test                            Test the package.
dist                            Prepare the distribution package by building, testing and running it.
tag                             Tag the package on GitHub.
upload                          Upload the package to GitHub.
```

Issue this to run the GUI:

```
$ make run
```

### Installing the binary package <a name="installing-binary-package" />

You can either create it by cloning the Git repo and then:

```
$ make dist
```

The binary package will be in the `dist` folder.

Or you can download the binary package from the [releases](https://github.com/paulissoft/pato-gui/releases).

In either case install the binary in your system environment.

## Usage <a name="usage" />

### Launch the GUI <a name="launch-the-gui" />

Via the command line in the root of `pato-gui`:

```
$ make run
```

Or:

```
$ python3 src/pato_gui/app.py
```

Or launch the program if you installed the binary package.

A graphical interface will pop up.

### Problems <a name="problems" />

You may encounter problems in the GUI like:

```
INFO:Version of "mvn" is "3.8.7" and its location is "/usr/local/bin"
INFO:Version of "perl" is "5.30.3" and its location is "/usr/bin"
Traceback (most recent call last):
  File "/Users/gpaulissen/dev/pato-gui/build/pato-gui/macos/app/PatoGui.app/Contents/Resources/app/pato_gui/app.py", line 410, in <module>
    main()
  File "/Users/gpaulissen/dev/pato-gui/build/pato-gui/macos/app/PatoGui.app/Contents/Resources/app/pato_gui/app.py", line 397, in main
    argv, logger, args = initialize()
  File "/Users/gpaulissen/dev/pato-gui/build/pato-gui/macos/app/PatoGui.app/Contents/Resources/app/pato_gui/app.py", line 123, in initialize
    args.mvnd = 'mvnd' in check_environment()
  File "/Users/gpaulissen/dev/pato-gui/build/pato-gui/macos/app/PatoGui.app/Contents/Resources/app/pato_gui/app.py", line 151, in check_environment
    assert not (p[5]) or proc.returncode == 0, proc.stderr
AssertionError: /bin/sh: sql: command not found
```

The last line says that `sql` can not be found on the PATH.

First find out where it should be found in a normal command line prompt:

```
$ which sql
```

Please note that on Windows you must use `where`.

Output:

```
/opt/oracle/sqlcl/bin/sql
```

On Windows just change your user PATH.

On a Mac it is a bit more complicated.

So we need to add `/opt/oracle/sqlcl/bin` to the system PATH list (active for applications in `/Applications`).

What is the default list? Here some possibilities:

```
$ sudo launchctl dumpstate | grep PATH | sort -u
```

The output of this includes this short line, the default list:

```
PATH => /usr/bin:/bin:/usr/sbin:/sbin
```

So finally add the path of `sql`:

```
$ sudo launchctl config user path /usr/bin:/bin:/usr/sbin:/sbin:/opt/oracle/sqlcl/bin
```

You must reboot for changes to take effect.

### Help <a name="help" />

From the command line:

```
$ python3 src/pato_gui/app.py -h
```

Output like:

```
usage: app.py [-h] [-d] [--db-config-dir DB_CONFIG_DIR] [file]

Setup logging

positional arguments:
  file                  The POM file

options:
  -h, --help            show this help message and exit
  -d                    Enable debugging
  --db-config-dir DB_CONFIG_DIR
                        The database configuration directory
```

And in the left top corner of the GUI screen there is a Help button.

### Examples <a name="examples" />

Start a POM file, skipping the first GUI screen:

```
$ python3 src/pato_gui/app.py /path/to/pom.xml
```
