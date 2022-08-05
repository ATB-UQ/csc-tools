from setuptools import setup, find_packages

from csc import __version__

setup(
    name='csc_tools',
    version=__version__,

    url='https://github.com/ATB-UQ/csc-validator',
    author='Sharif Nada',
    author_email='s.nada@uq.edu.au',

    packages=find_packages(),

    install_requires=[
    'pyyaml',
    ],

    entry_points={
    'console_scripts': [
        #'csc-validate=csc_tools.validate:cmd_validate',
        'csc=csc.csc:main',
        ],
    },
)