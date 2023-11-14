# -*- coding: utf-8 -*-
from importlib.metadata import metadata

__all__ = ['__package_name__', '__version__', '__title__', '__author__', '__email__', '__license__', '__copyright__', '__url__', '__help_url__']


pato_gui_metadata = metadata('pato-gui')
__package_name__ = pato_gui_metadata["Name"]
__version__ = pato_gui_metadata["Version"]
__title__ = pato_gui_metadata["Summary"]
__author__ = pato_gui_metadata["Author"]
__email__ = pato_gui_metadata["Author-email"]
__license__ = pato_gui_metadata["License"]
__url__ = pato_gui_metadata["Project-URL"][len("Repository, "):]
__help_url__ = pato_gui_metadata["Home-page"]
# Can not be set via metadata
__copyright__ = "Copyright (c) 2021-2023 Gert-Jan Paulissen"


def version():
    print(__version__)


def main():
    for var in __all__:
        try:
            print("%s: %s" % (var, eval(var)))
        except NameError:
            pass


if __name__ == '__main__':
    main()
