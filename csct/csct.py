import click

from csct import __version__

from .validate.validate import validate

#main CLI
@click.group()
@click.version_option(__version__)
def cli():
    pass

#commands
cli.add_command(validate)