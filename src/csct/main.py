import importlib.metadata

import click

from . import csct

__version__ = importlib.metadata.version('csc_tools')

#main CLI
@click.group()
@click.version_option(__version__) #show version information
def cli():
    pass

#top-level commands
cli.add_command(csct.upload.upload)
cli.add_command(csct.validate.validate)