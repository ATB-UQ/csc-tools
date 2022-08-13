import os
from pathlib import Path
import click
import yaml
import cerberus

from .schema import get_metadata_schema

def find_directories(dirs):
    found_dirs = set()
    for dir in dirs:
        found_dirs.update(x[0] for x in os.walk(dir) \
            if (Path(x[0]) / 'atbrepo.yaml').is_file() or \
                (Path(x[0]) / 'atbrepo.yml').is_file() #or \
                #(Path(x[0]) / 'metadata.yaml').is_file() or \
                #(Path(x[0]) / 'metadata.yml').is_file()
                )
    return found_dirs

def validate_metadata(dirs):
    click.echo("Validating metadata files in dataset paths...")
    for dir in dirs:
        click.echo(f"{dir}          ", nl=False)
        metadata_path = os.path.join(dir, "atbrepo.yml") #check for this name first
        if not os.path.exists(metadata_path): #if it's not there...
            metadata_path = os.path.join(dir, "atbrepo.yaml") #check for the alternative name
        try: 
            with open(metadata_path, "r") as c: #try to open the metadata file
                raw_metadata = yaml.safe_load(c) #if the metadata file is there, create the raw_config dictionary by loading the yaml file
        except: 
            click.secho("FAIL", fg='red')
            raise Exception(f"Could not open metadata file in path: {metadata_path}") #throw exception if it's not there
    #test_metadata = {'title': '', 'organization': 'mduqf'}
        validator = cerberus.Validator(get_metadata_schema())
        validator.validate(raw_metadata)

        if validator.errors:
            click.secho("FAIL", fg='red')
            [click.secho(f"{key}: {value}", fg='red') for key, value in validator.errors.items()]
        else:
            click.secho("PASS", fg='green')


@click.command()
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def validate(dirs):
    """
    Docstring.
    """
    found_dirs = find_directories(dirs)

    if found_dirs:
        click.echo("Located datasets in the following paths:")
        click.echo("\n".join(find_directories(dirs)))
    else:
        click.secho("No datasets could be located in the supplied paths:", fg='red')
        click.echo("\n".join(dirs))
        raise click.Abort()

    validate_metadata(found_dirs)    