from setuptools import setup
from Cython.Build import cythonize

import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

setup(
    ext_modules=cythonize(
        'raycasting.pyx', annotate=True, language_level=3), # enables generation of the html annotation file
)
