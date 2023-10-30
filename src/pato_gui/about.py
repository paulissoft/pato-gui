# -*- coding: utf-8 -*-

import sys
try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata


# Find the name of the module that was used to start the app
# Hard code value for app_module, otherwise "briefcase dev --test" gives
# E importlib.metadata.PackageNotFoundError: No package metadata was found for tests
app_module = 'pato_gui'  # sys.modules['__main__'].__package__
# Retrieve the app's metadata
metadata = importlib_metadata.metadata(app_module)

__title__ = metadata['Formal-Name']
# __package_name__ = 'pato-gui'
__author__ = metadata['Author']
__description__ = metadata['Summary']
__email__ = metadata['Author-email']
__version__ = '3.2.0'
__version_info__ = tuple(__version__.split("."))
__license__ = 'MIT License'
__copyright__ = 'Copyright (c) 2021-2023 Gert-Jan Paulissen'
__url__ = metadata['Home-page']
__help_url__ = "https://paulissoft.github.io/pato-gui"

if __name__ == '__main__':
    print(__version__)
