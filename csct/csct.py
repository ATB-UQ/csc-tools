import click

from csct import __version__

from .validate.validate import validate

#main CLI
@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
    pass

#commands
cli.add_command(validate)