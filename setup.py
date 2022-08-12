from setuptools import setup, find_packages

from csct import __version__

setup(
    name='csc_tools',
    version=__version__,

    url='https://github.com/ATB-UQ/csc-tools',
    author='Sharif Nada',
    author_email='s.nada@uq.edu.au',

    packages=find_packages(),

    install_requires=[
    'pyyaml',
    'click',
    ],

    entry_points={
    'console_scripts': [
        'csct=csct.csct:cli',
        ],
    },
)