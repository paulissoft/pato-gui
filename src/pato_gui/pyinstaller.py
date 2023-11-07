import PyInstaller.__main__
from pathlib import Path


def install():
    HERE = Path(__file__).parent.absolute()
    path_to_main = str(HERE / "program.py")
    PyInstaller.__main__.run([
        path_to_main,
        '--onefile',
        '--windowed',
        # other pyinstaller options... 
    ])
