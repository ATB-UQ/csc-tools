import click

import csct.common

@click.group(short_help="Execute server-side commands when running csct on the repository server.")
def server():
    """
    Execute server-side commands when running csct on the repository server.
    """
    pass

@click.command(short_help="Commit changes to a dataset.")
def commit():
    pass
