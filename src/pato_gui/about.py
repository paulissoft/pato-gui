# -*- coding: utf-8 -*-

try:
    import tomllib
except ImportError:
    import tomli as tomllib

__all__ = ['__package_name__', '__version__', '__title__', '__author__', '__email__', '__license__', '__copyright__', '__url__', '__help_url__']

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
    __package_name__ = data['tool']['poetry']['name']
    __version__ = data['tool']['poetry']['version']
    __title__ = data['tool']['poetry']['description']
    author_email = data['tool']['poetry']['authors'][0]
    __author__ = author_email[0:author_email.find(' <')]
    __email__ = author_email[author_email.find(' <') + 2:-1]
    __license__ = data['tool']['poetry']['license']
    # Can not be set in pyproject.toml
    __copyright__ = "Copyright (c) 2021-2023 Gert-Jan Paulissen"
    __url__ = data['tool']['poetry']['repository']
    __help_url__ = data['tool']['poetry']['homepage']


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
