__author__ = 'dimv36'
application_title = "MyWallet"   # what you want to application to be called
main_python_file = "main.py"     # the name of the python file you use to run the program

import sys

from cx_Freeze import setup, Executable

base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

includes = ['lxml.etree', 'lxml._elementpath', 'inspect', 'gzip']

setup(
    name=application_title,
    version="0.1",
    description="MyWallet",
    options={"build_exe": {"includes": includes}},
    executables=[Executable(main_python_file, base=base)]
    )
