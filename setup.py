"""run this
python setup.py sdist
pip install .
"""

# from distutils.core import setup
from setuptools import setup, find_packages
from src.fastdataing import __version__

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt","r") as f:
    required = f.read().splitlines()

version = __version__()

setup(
name         = 'fastdataing',
version      = version,
py_modules   = ['fastdataing'],
author       = 'CHENDONGSHENG',
author_email = 'eastsheng@hotmail.com',
packages=find_packages('src'),
package_dir={'': 'src'},
install_requires=required,
url          = 'https://github.com/eastsheng/fastdataing',
description  = 'Read themo info from lammps output file or log file',
long_description=long_description,
long_description_content_type='text/markdown'
)

