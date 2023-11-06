# -*- coding: utf-8 -*-

import pkgutil
import re

__all__ = ['__package_name__', '__version__', '__version_info__', '__title__', '__author__', '__email__', '__license__', '__copyright__', '__url__', '__help_url__']


toml = pkgutil.get_data('pato_gui', "../../pyproject.toml").decode("utf-8")

name_regexp = re.compile(r'''^name = "([^"]*)"''', re.M)
match = name_regexp.search(toml)
assert match, "Unable to find name string in pyproject.toml"
__package_name__ = match.group(1)

version_regexp = re.compile(r'''^version = "([^"]*)"''', re.M)
match = version_regexp.search(toml)
assert match, "Unable to find version string in pyproject.toml"
__version__ = match.group(1)
__version_info__ = __version__.split('.')

description_regexp = re.compile(r'''^description = "([^"]*)"''', re.M)
match = description_regexp.search(toml)
assert match, "Unable to find description string in pyproject.toml"
__title__ = match.group(1)

authors_regexp = re.compile(r'''^authors = \["([^<"]*)(<([^>])*>)?"\]''', re.M)
match = authors_regexp.search(toml)
assert match, "Unable to find authors string in pyproject.toml"
__author__ = match.group(1)
__email__ = match.group(3)

license_regexp = re.compile(r'''^license = "([^"]*)"''', re.M)
match = license_regexp.search(toml)
assert match, "Unable to find license string in pyproject.toml"
__license__ = match.group(1)

__copyright__ = 'Copyright (c) 2021-2023 Gert-Jan Paulissen'
__url__ = "https://github.com/paulissoft/pato-gui"
__help_url__ = "https://paulissoft.github.io/pato-gui"

if __name__ == '__main__':
    print(__version__)
