import click
import sys

@click.command(short_help="View and edit dataset metadata.")
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
@click.option('-create', 'action', is_flag=True, flag_value='create', help="Validate all dataset properties. [default]")
@click.option('-delete', 'action', is_flag=True, flag_value='delete', help="Validate all dataset properties and attempt to export dataset.")
@click.option('-modify', 'action', is_flag=True, flag_value='modify', help="Validate configuration settings.")
@click.option('-view', 'action', is_flag=True, flag_value='view', help="Validate configuration settings and dataset metadata.")
@click.option('-list', 'action', is_flag=True, flag_value='list', help="Validate dataset subdirectory structure.")
@click.option('-summary', 'action', is_flag=True, flag_value='summary', help="Validate dataset subdirectory structure and files.")
def metadata(action, dirs):
    """
    View and modify metadata.

    \b
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    def info(action):
        click.echo(getattr(sys.platform, action)())
    info(action)