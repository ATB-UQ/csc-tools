import os
from pathlib import Path
import click
import yaml
import cerberus
import sys

from .schema import *

global pass_echo
pass_echo = click.style(f"{'PASSED': <8}", fg='green')
global fail_echo
fail_echo = click.style(f"{'FAILED': <8}", fg='red')

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
        click.echo("\n".join(dirs))
        raise click.Abort()            
    return found_dirs

@click.group()
@click.pass_context
def validate(ctx):
    """
    Validate dataset metadata, directory structure, and contents
    """
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand. Defaulting to all')
        
        validate_all(ctx)
           

@validate.command('all')
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def validate_all(dirs):
    """
    Validate dataset metadata, directory structure, and contents.
    """

    found_dirs = find_directories(dirs)
    validate_metadata(found_dirs)
    validate_directory(found_dirs)

@validate.command('metadata')
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def validate_metadata(dirs):
    """
    Validate dataset metadata.
    """
    
    found_dirs = find_directories(dirs)

    click.echo("Validating metadata files in dataset paths...")
    
    for dir in found_dirs:
        dir_echo = click.style(Path(dir).resolve())

        if (Path(dir) / "atbrepo.yaml").exists() and (Path(dir) / "atbrepo.yml").exists(): #check for duplicate metadata files
            click.secho(f"{fail_echo}{dir_echo}")
            click.secho(f"Two metadata files found in path.  Only one metadata file per dataset is supported.", fg='red')
            continue
        else:
            metadata_path = Path(dir) / "atbrepo.yaml" #check for this name first
            if not metadata_path.exists(): #if it's not there...
                metadata_path = Path(dir) / "atbrepo.yml" #check for the alternative name
            try: 
                with open(metadata_path, "r") as c: #try to open the metadata file
                    metadata = yaml.safe_load(c) #if the metadata file is there, create the raw_config dictionary by loading the yaml file
            except: 
                click.secho(f"{fail_echo}{dir_echo}")
                click.secho(f"Could not open metadata file in path: {metadata_path}", fg='red')
                sys.exit()
        
        validator = cerberus.Validator(get_metadata_schema())
        validator.validate(metadata)

        if validator.errors:
            click.secho(f"{fail_echo}{dir_echo}")
            [click.secho(f"{key}: {value[0]}", fg='red') for key, value in validator.errors.items()]
        else:
            click.secho(f"{pass_echo}{dir_echo}")

@validate.command('directory')
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))            
def validate_directory(dirs):
    """
    Validate dataset directory structure.
    """
    
    found_dirs = find_directories(dirs)

    click.echo("Validating directory structure in dataset paths...")

    for dir in found_dirs:
        dir_echo = click.style(dir)
        
        directory_structure = {}
   
        for subdir in Path(dir).glob('*'):
            if subdir.exists() and str(subdir.name) not in ["atbrepo.yaml", "atbrepo.yml"]: 
                if subdir.is_file():
                    directory_structure[str(subdir.name)] = 'file'
                elif subdir.is_dir():
                    directory_structure[str(subdir.name)] = 'directory'
                else:
                    directory_structure[str(subdir.name)] = 'other'           


        validator = DirectoryValidator(get_directory_schema())
        validator.validate(directory_structure)

        if validator.errors:
            click.secho(f"{fail_echo}{dir_echo}")
            [click.secho(f"{key}: {value[0]}", fg='red') for key, value in validator.errors.items()]
        else:
            click.secho(f"{pass_echo}{dir_echo}")