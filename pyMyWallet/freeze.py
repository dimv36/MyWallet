__author__ = 'dimv36'
import sys
from cx_Freeze import setup, Executable

application_title = "MyWallet"   # what you want to application to be called
main_python_file = "main.py"     # the name of the python file you use to run the program

base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ['inspect', 'gzip']

setup(
    name=application_title,
    version="0.1",
    description="MyWallet",
    options={"build_exe": {"includes": includes}},
    executables=[Executable(script=main_python_file,
                            base=base,
                            compress=False,
                            copyDependentFiles=True,
                            appendScriptToExe=True,
                            appendScriptToLibrary=False,
                            icon='icons/wallet.ico'
                            )
                 ]
    )
