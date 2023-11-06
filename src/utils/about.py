# -*- coding: utf-8 -*-

"""
import pkgutil
import re

version_regexp = re.compile(r'''^version = "([^"]*)"''', re.M)

data = pkgutil.get_data(__package__, "../pyproject.toml")
match = version_regexp.search(data.decode("utf-8"))
if match:
    __version__ = match.group(1)
else:  # pragma: no cover
    raise RuntimeError("Unable to find version string")
"""

__title__ = 'Paulissoft Application Tools for Oracle (PATO) GUI'
__package_name__ = 'pato-gui'
__author__ = "Gert-Jan Paulissen"
__description__ = ' '.join('''
Paulissoft Application Tools for Oracle (PATO) GUI.
'''.strip().split())
__email__ = "paulissoft@gmail.com"
__version_info__ = ('3', '2', '0')
__version__ = '.'.join(__version_info__)
__license__ = "MIT License"
__copyright__ = 'Copyright (c) 2021-2023 Gert-Jan Paulissen'
__url__ = "https://github.com/paulissoft/pato-gui"
__help_url__ = "https://paulissoft.github.io/pato-gui"

if __name__ == '__main__':
    print(__version__)
