#coding=cp936

# from distutils.core import setup
# import py2exe
# import sys
# import os
# import glob
# import sys
# this allows to run it with a simple double click.
# sys.argv.append('py2exe')

# py2exe_options={
		# "includes":["sip" , "PyQt5.QtCore" , "PyQt5.QtGui" , "encodings"],
		# "dll_excludes":["MSVCP90.dll",],
		# "compressed":1,
		# "optimize":2,
		# "ascii":0,
		# "bundle_files":1
		# }
		
# setup(
		# name='Python',
		# version='1.0',
		# windows=[
				# 'mainWindow.py',
				# 'scoreWindow.py',
				# 'SpiderForSchoolWeb.py',
				# ],
		# zipfile=None,
		# options={"py2exe":py2exe_options}
		# )
import sys
from cx_Freeze import setup, Executable

build_exe_options = {"optimize": 2,
                     "include_files": ["scoreWindow.py" , "SpiderForSchoolWeb.py","../doc/user.txt","../img/image.gif"]}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [Executable(script='mainWindow.py',
               base=base,
               targetName="Demo.exe",
               compress=True)]

setup(name='Spider',
      version='0.1',
      description='Sample cx_Freeze wxPython script',
      options = {"build_exe": build_exe_options},
      executables=executables)