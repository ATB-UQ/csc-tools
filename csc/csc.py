import sys
from . import config
import argparse
from csc import __version__

def main(command_line=None):
    parser = argparse.ArgumentParser(
        prog='csc',
        description="Australian Computational and Simulation Commons command line tools (csc-tools)."
        )
    
    parser.add_argument(
        '-v', '--version', 
        action='version',
        version='%(prog)s version {version}'.format(version=__version__)
        )    
    
    subparsers = parser.add_subparsers(dest='command')

    config_parser = subparsers.add_parser('config', help="List or modify configuration options")
    config_parser.add_argument(
        'list',
        help="List current configuration options"
    )

    args = parser.parse_args(command_line)