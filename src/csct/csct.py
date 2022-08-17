import click

from .validate.validate import validate

import importlib.metadata

__version__ = importlib.metadata.version('csc_tools')

#main CLI
@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
    pass

#commands
cli.add_command(validate)