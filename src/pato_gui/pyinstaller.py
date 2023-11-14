import PyInstaller.__main__
from pathlib import Path


def install():
    HERE = Path(__file__).parent.absolute()
    spec_file = str(HERE / "PatoGui.spec")
    PyInstaller.__main__.run([
        spec_file
    ])
