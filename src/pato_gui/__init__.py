import sys
try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata
    
# pato_gui needed for testing
for app_module in [sys.modules['__main__'].__package__ , 'pato_gui']:
    # Retrieve the app's metadata
    try:
        metadata = importlib_metadata.metadata(app_module)
        if 'Formal-Name' in metadata:
            break
    except importlib_metadata.PackageNotFoundError as err:
        pass
    

__title__ = metadata['Formal-Name'] if metadata['Formal-Name'] else "PatoGui"
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

