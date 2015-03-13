# setup.py
from distutils.core import setup
import py2exe
import glob
      
setup(console=["main.py"],data_file=["graphics","sound",glob.glob("*.bmp"),glob.glob(".txt")])

