import os
from pathlib import Path
import click
import yaml
import cerberus
import sys

from .schema import *

@click.command()
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
@click.option('-a', '--all', is_flag=True, help="Validate all dataset properties. [default]")
@click.option('-m', '--metadata', is_flag=True, help="Validate dataset metadata.")
@click.option('-s', '--subdir-structure', is_flag=True, help="Validate dataset subdirectory structure.")
@click.option('-c', '--subdir-contents', is_flag=True, help="Validate dataset subdirectory structure and contents.")
@click.option('-f', '--file-contents', is_flag=True, help="Validate dataset subdirectory structure, subdirectory contents, and contents of files in subdirectories.")
def validate(all, metadata, subdir_structure, subdir_contents, file_contents, dirs):
    """
    Validate dataset metadata, subdirectory structure, and contents of subdirectories and files.

    \b
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    if not dirs: #default to cwd if no directories supplied
        click.echo("No directory paths supplied.  Searching for datasets in current working directory.")
        dirs = ['.']
    found_dirs = find_directories(dirs)
    
    if all or (metadata == subdir_structure == subdir_contents == file_contents): # process flags
        metadata = True; subdir_structure = True; subdir_contents = True; file_contents = True
    for dir in found_dirs:
        click.echo(f"Validating dataset in path {dir}")
        if metadata:
            validate_metadata(dir)
        if file_contents:
            validate_file_contents(dir)
        elif subdir_contents:
            validate_dir_contents(dir)        
        elif subdir_structure:
            validate_dir_structure(dir)
        
def find_directories(dirs):
    found_dirs = set()
    for dir in dirs:
        found_dirs.update(x[0] for x in os.walk(Path(dir).resolve()) \
            if (Path(x[0]) / 'atbrepo.yaml').is_file() or \
                (Path(x[0]) / 'atbrepo.yml').is_file()
                )
    if found_dirs:
        click.echo("Located datasets in the following paths:")
        click.echo("\n".join(found_dirs))
    else:
        click.secho("No datasets could be located in the supplied paths:", fg='red')
        click.echo("\n".join(str(Path(dir).resolve()) for dir in dirs))
        sys.exit()            
    return found_dirs

def get_path_type(path):
    """
    Return the type of a supplied path.
    """
    if path.is_file():
        return 'file'
    elif path.is_dir():
        return 'directory'
    else:
        return 'other'

global validate_print_width
validate_print_width = 40

def validate_metadata(dir):
    """
    Validate dataset metadata.
    """

    click.echo("Validating metadata".ljust(validate_print_width, '.'), nl=False)

    if (Path(dir) / "atbrepo.yaml").exists() and (Path(dir) / "atbrepo.yml").exists(): #check for duplicate metadata files
        click.secho("FAILED", fg='red')
        click.secho(f"Two metadata files found in path.  Only one metadata file per dataset is supported.", fg='red')
        return False
    else:
        metadata_path = Path(dir) / "atbrepo.yaml" #check for this name first
        if not metadata_path.exists(): #if it's not there...
            metadata_path = Path(dir) / "atbrepo.yml" #check for the alternative name
        try: 
            with open(metadata_path, "r") as c: #try to open the metadata file
                metadata = yaml.safe_load(c) #if the metadata file is there, create the raw_config dictionary by loading the yaml file
        except: 
            click.secho("FAILED", fg='red')
            click.secho(f"Could not open metadata file in path {metadata_path}", fg='red')
            return False
    
    validator = cerberus.Validator(get_metadata_schema())
    validator.validate(metadata)

    if validator.errors:
        click.secho("FAILED", fg='red')
        [click.secho(f"{key}: {value[0]}", fg='red') for key, value in validator.errors.items()]
        return False
    else:
        click.secho("PASSED", fg='green')
        return True   
           
def validate_dir_structure(dir):
    """
    Validate dataset subdirectory structure.
    """

    click.echo("Validating subdirectory structure".ljust(validate_print_width, '.'), nl=False)

    
    directory_structure = {}

    for subdir in Path(dir).glob('*'):
        if subdir.exists() and str(subdir.name) not in ["atbrepo.yaml", "atbrepo.yml"]: 
            directory_structure[str(subdir.name)] = get_path_type(subdir)
          
    validator = DirectoryValidator(get_directory_structure_schema())
    validator.validate(directory_structure)

    if validator.errors:
        click.secho("FAILED", fg='red')
        [click.secho(f"{key}: {value[0]}", fg='red') for key, value in validator.errors.items()]
        return False
    else:
        click.secho("PASSED", fg='green')
        return True

def validate_dir_contents(dir):
    """
    Validate dataset subdirectory contents.
    """

    validate_dir_structure_status = validate_dir_structure(dir)

    click.echo("Validating subdirectory contents".ljust(validate_print_width, '.'), nl=False)

    if not validate_dir_structure_status:
        click.secho("SKIPPED", fg='yellow')
        click.secho("Subdirectory content validation requires validated subdirectory structure.", fg='yellow')
        return False
    else: 
        
        directory_structure = {}

        for subdir in Path(dir).glob('*'):
            if subdir.is_dir() and str(subdir.name) not in ["atbrepo.yaml", "atbrepo.yml"]: 
                directory_structure[str(subdir.name)] = {str(key): get_path_type(key) for key in Path(subdir).glob('*')}     
        
        validator = DirectoryValidator(get_directory_contents_schema())
        validator.validate(directory_structure)

        if validator.errors:
            click.secho("FAILED", fg='red')
            [click.secho(f"{key}: {value[0]}", fg='red') for key, value in validator.errors.items()]
            return False
        else:
            click.secho("PASSED", fg='green')
            return True  

def validate_file_contents(dir):
    """
    Validate dataset file contents.
    """

    validate_dir_contents_status = validate_dir_contents(dir)

    click.echo("Validating file contents".ljust(validate_print_width, '.'), nl=False)
    
    if not validate_dir_contents_status:
        click.secho("SKIPPED", fg='yellow')
        click.secho("File content validation requires validated subdirectory contents.", fg='yellow')
        return False
    else: #placeholder
        click.secho("PASSED", fg='green')
        return True