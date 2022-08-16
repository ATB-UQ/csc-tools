from setuptools import setup, find_packages

from csct import __version__

setup(
    name='csc_tools',
    version=__version__,

    url='https://github.com/ATB-UQ/csc-tools',
    author='Sharif Nada',
    author_email='s.nada@uq.edu.au',

    packages=find_packages(),

    python_requires='>=3.6',

    install_requires=[
    'setuptools>=61.2',
    'pyyaml>=6.0',
    'click>=8.1',
    'cerberus>=1.3',
    ],

    entry_points={
    'console_scripts': [
        'csct=csct.csct:cli',
        ],
    },
)