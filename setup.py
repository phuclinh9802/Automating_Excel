from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize('data_cython.py'), requires=['xlrd'])