import importlib.metadata

import click

import csct.config, csct.validate

__version__ = importlib.metadata.version('csc_tools')


#main CLI
@click.group()
@click.version_option(__version__) #show version information
def cli():
    pass

#top-level commands
cli.add_command(csct.config.config)
cli.add_command(csct.validate.validate)

if __name__ == "__main__":
   cli()