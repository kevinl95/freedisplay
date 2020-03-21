import sys
from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "pathos", "multiprocess", "multiprocess.context", "jinja2.ext"],
    "excludes": [""],
    "include_files": [
        "static",
        "templates",
    ],
}

base = "console"

setup(
    name="FreeDisplay",
    version="1.0",
    description="Share your screen over your local network!",
    author="Kevin Loeffler",
    targetName="freedisplay.app",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon = 'images/displayicon.icns')],
)
