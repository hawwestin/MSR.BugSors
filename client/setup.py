import sys
from cx_Freeze import setup, Executable
import cx_Freeze
import tkinter

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("BugSors_Main.py", base=base)]
build_exe_options = {"includes": ["tkinter"]}

cx_Freeze.setup(
    name='client_py',
    version='1.0.0',
    url='https://bitbucket.org/pap20170414/pap',
    options={"build_exe": {"includes": ["tkinter"]}},
    author='Michal Robaszewski',
    author_email='michal.robaszewski@gmail.com',
    description='BugSors',
    executables=executables
)
