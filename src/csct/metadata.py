import click
import sys

@click.group(short_help="View and edit dataset metadata.")
def metadata():
    """
    View and edit dataset metadata.
    """
    pass

@click.command(short_help="Add a new metadata field.")
@click.argument('name', required=True, type=str)
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def add(name, value, dirs):
    """
    Add a new metadata field.

    \b
    NAME    The metadata field name to be created.
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    print(name, value, dirs)

@click.command(short_help="Add a value to an existing metadata field.")
@click.argument('name', required=True, type=str)
@click.argument('value', required=True, type=str)
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def assign(name, value, dirs):
    """
    Assign a new value to a metadata field.  For fields that only accept a single value, the field must not already have a value assigned.  For fields that accept a list of values, the value supplied will be appended to the existing list of values.  

    \b
    NAME    The metadata field name to which a value will be added.
    VALUE   The value to be added to the supplied field name.
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    print(name, value, dirs)

@click.command(short_help="Modify an existing metadata value.")
@click.argument('name', required=True, type=str)
@click.argument('old', required=True, type=str)
@click.argument('new', required=True, type=str)
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def modify(name, value, dirs):
    """
    Modify the value of an existing metadata field.

    \b
    NAME    The metadata field to be modified.
    OLD     The metadata value to be replaced.
    NEW     The new metadata value to be added.
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    pass

@click.command(short_help="Remove existing metadata values or fields. ")
@click.argument('name', required=True, nargs=1)
@click.option('-r', '--remove-field', is_flag=True, help="If specified, the metadata field itself will also be removed.")
@click.option('-v', '--value', multiple=True, type=str, help="Specify a specific value to be removed.  May be used multiple times to specify multiple values.")
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def remove(name, value, dirs):
    """
    Remove existing metadata values or fields.  
    
    If --value is not specified, all values associated with the field name will be removed.

    \b
    NAME    The metadata field name from which values will be removed.
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    pass

@click.command(short_help="Rename an existing metadata field, leaving its values intact.")
@click.argument('name', required=True, type=str)
@click.argument('old', required=True, type=str)
@click.argument('new', required=True, type=str)
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def rename(name, value, dirs):
    """
    Rename an existing metadata field, leaving its values intact.

    \b
    OLD     The metadata field name to be replaced.
    NEW     The new metadata field name.
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    pass


metadata.add_command(add)
metadata.add_command(assign)
metadata.add_command(modify)
metadata.add_command(remove)
metadata.add_command(rename)