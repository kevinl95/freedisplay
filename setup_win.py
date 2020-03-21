import sys
from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ["TCL_LIBRARY"] = os.path.join(PYTHON_INSTALL_DIR, "tcl", "tcl8.6")
os.environ["TK_LIBRARY"] = os.path.join(PYTHON_INSTALL_DIR, "tcl", "tk8.6")

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "pathos", "multiprocess", "multiprocess.context", "jinja2.ext"],
    "excludes": [""],
    "include_files": [
        "static",
        "templates",
        os.path.join(PYTHON_INSTALL_DIR, "DLLs", "tk86t.dll"),
        os.path.join(PYTHON_INSTALL_DIR, "DLLs", "tcl86t.dll"),
    ],
}

base = "console"

setup(
    name="FreeDisplay",
    version="1.0",
    description="Share your screen over your local network!",
    author="Kevin Loeffler",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)],
)
