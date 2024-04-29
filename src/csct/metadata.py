import click

import csct.common

@click.group(short_help="View and edit dataset metadata.")
def metadata():
    """
    View and edit dataset metadata.
    """
    pass

@click.command(short_help="Add a new metadata field.")
@click.argument('name', required=True, type=str)
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def add(name, dirs):
    """
    Add a new metadata field.

    \b
    NAME    The metadata field name to be created.
    DIRS    Directories to recursively scan for metadata files. 
            [default: current working directory]
    """
    print(name, dirs)

@click.command(short_help="Add a value to an existing metadata field.")
@click.argument('name', required=True, type=str)
@click.argument('value', required=True, type=str)
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def assign(name, value, dirs):
    """
    Assign a new value to a metadata field.  For fields that only accept a single value, the field must not already have a value assigned.  For fields that accept a list of values, the value supplied will be appended to the existing list of values.  

    \b
    NAME    The metadata field name to which a value will be added.
    VALUE   The value to be added.
    DIRS    Directories to recursively scan for metadata files. 
            [default: current working directory]
    """
    print(name, value, dirs)

@click.command(short_help="Modify a metadata value.")
@click.argument('name', required=True, type=str)
@click.argument('oldvalue', required=True, type=str)
@click.argument('newvalue', required=True, type=str)
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def modify(name, oldvalue, newvalue, dirs):
    """
    Modify the value of an existing metadata field.

    \b
    NAME        The metadata field to be modified.
    OLDVALUE    The metadata value to be replaced.
    NEWVALUE    The new metadata value to be added.
    DIRS        Directories to recursively scan for metadata files. 
                [default: current working directory]
    """
    print(name, oldvalue, newvalue, dirs)

@click.command(short_help="Remove existing metadata values or fields.")
@click.argument('name', required=True, nargs=1)
@click.option('-v', '--value', multiple=True, type=str, help="Specify a value to be removed.  May be used multiple times to specify multiple values.  If not specified, all values associated with the supplied field name will be removed.")
@click.option('-r', '--remove-field', is_flag=True, help="If specified, the metadata field itself will be removed, in addition to all of its associated values.")
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def remove(name, remove_field, value, dirs):
    """
    Remove existing metadata values or fields.  

    \b
    NAME    The metadata field name from which values will be removed.
    DIRS    Directories to recursively scan for metadata files. 
            [default: current working directory]
    """
    print(name, remove_field, value, dirs)

@click.command(short_help="Rename an existing metadata field, leaving its values intact.")
@click.argument('oldname', required=True, type=str)
@click.argument('newname', required=True, type=str)
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def rename(oldname, newname, dirs):
    """
    Rename an existing metadata field, leaving its values intact.

    \b
    OLDNAME    The metadata field name to be replaced.
    NEWNAME    The new metadata field name.
    DIRS       Directories to recursively scan for metadata files. 
               [default: current working directory]
    """
    pass

@click.command(short_help="View the metadata of a dataset or datasets.")
@click.option('-d', '--by-dataset', 'view_type', flag_value='by_dataset', default=True, help="View metadata field names and values, listing the metadata for each dataset sequentially. [default]")
@click.option('-m', '--by-metadata', 'view_type', flag_value='by_value', help="View metadata of datasets grouped by metadata value, listing the datasets matching each name and value combination.")
@click.option('-c', '--count', 'view_type', flag_value='count', help="View a count of datasets matching each metadata name and value combination.")
@click.option('-n', '--name', type=str, multiple=True, help="Only display results matching a specified metadata field name.  Can be used multiple times to specify multiple names.")
@click.option('-v', '--value', type=str, multiple=True, help="Only display results matching a specified metadata field value. Can be used multiple times to specify multiple values.")
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def view(view_type, name, value, dirs):
    """
    View the metadata of a dataset or datasets.

    \b
    DIRS       Directories to recursively scan for metadata files. 
               [default: current working directory]
    """
    print(name, value, dirs, view_type)   
    found_dirs = csct.common.find_directories(dirs)

metadata.add_command(add)
metadata.add_command(assign)
metadata.add_command(modify)
metadata.add_command(remove)
metadata.add_command(rename)
metadata.add_command(view)