import sys
from . import config
import argparse
from csct import __version__

prog_name = 'csct'

class main(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog=prog_name,
            usage="""%(prog)s <command> [<args>]

Available commands:

Configure csc-tools:
    config      List or modify configuration options
    init        Initialize a new csc-tools instance

Create a new dataset directory tree:
    clone       Clone the directory structure and metadata of a dataset into a new directory tree
    create      Create an empty directory structure and initialize metadata
""")        
        parser.add_argument('command', choices=['config'], help=argparse.SUPPRESS)
        parser.add_argument(
            '-v', '--version', 
            action='version',
            version='%(prog)s version {version}'.format(version=__version__),
            help="show %(prog)s version number and exit"
        )
        #call help by default if no argument supplied 
        if len(sys.argv) <= 1:
            sys.argv.append('--help')
        #Read the first argument
        args = parser.parse_args(sys.argv[1:2])
        #use dispatch pattern to invoke method with same name of the argument
        getattr(self, args.command)()

    def config(self):
        parser = argparse.ArgumentParser(
            prog= prog_name + " config",
            usage="""%(prog)s <command> [<args>]

Arguments:
    list        List current configuration options
    locate      Print location of configuration file
"""
            )
        parser.add_argument('command', choices=['list','locate'], help=argparse.SUPPRESS)
        parser.add_argument('arguments', nargs='*', metavar='<args>', help="config arguments")
        #we are inside a subcommand, so ignore the first argument and read the rest
        args = parser.parse_args(sys.argv[2:])

        config.run_config(args.command, args.arguments)

#if __name__ == '__main__':
#    main()