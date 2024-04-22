import click
import sys

@click.group(short_help="View and edit dataset metadata.")
def metadata():
    pass

@click.command(short_help="Create new metadata field and/or assign a value to a field with no value.")
@click.option('-n', '--name', multiple=True, type=str, help="PLACEHOLDER")
@click.option('-v', '--value',  multiple=True, type=str, help="PLACEHOLDER")
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def add(name, value, dirs):
    """
    PLACEHOLDER

    \b
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    print(name, value, dirs)

@click.command(short_help="Delete the value of a metadata field or the field itself.")
@click.argument('name', nargs=1)
@click.argument('value', nargs=1)
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def delete(name, value, dirs):
    """
    PLACEHOLDER

    \b
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    pass

@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
@click.option('-create', 'action', is_flag=True, flag_value='create', help="Validate all dataset properties. [default]")
@click.option('-delete', 'action', is_flag=True, flag_value='delete', help="Validate all dataset properties and attempt to export dataset.")
@click.option('-modify', 'action', is_flag=True, flag_value='modify', help="Validate configuration settings.")
@click.option('-view', 'action', is_flag=True, flag_value='view', help="Validate configuration settings and dataset metadata.")
@click.option('-list', 'action', is_flag=True, flag_value='list', help="Validate dataset subdirectory structure.")
@click.option('-summary', 'action', is_flag=True, flag_value='summary', help="Validate dataset subdirectory structure and files.")
def test(action, dirs):
    """
    View and modify metadata.

    \b
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    def info(action):
        click.echo(getattr(sys.platform, action)())
    info(action)

metadata.add_command(add)
metadata.add_command(delete)