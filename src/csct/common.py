
import os
import pathlib
import sys
import yaml

import click

ckan_url = 'https://molecular-dynamics.atb.uq.edu.au/'

print_width = 40

def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()

def read_metadata_file(dir):

    if (pathlib.Path(dir) / "atbrepo.yaml").exists() and (pathlib.Path(dir) / "atbrepo.yml").exists():
        return None, f"Two metadata files found in path.  Only one metadata file per dataset is supported."
    else:
        metadata_path = pathlib.Path(dir) / "atbrepo.yaml" #check for this name first
        if not metadata_path.exists(): #if it's not there...
            metadata_path = pathlib.Path(dir) / "atbrepo.yml" #check for the alternative name
        try: 
            with open(metadata_path, "r") as c: #try to open the metadata file
                metadata = yaml.safe_load(c)
                return metadata, None
        except yaml.YAMLError:
            return None, f"Could not open metadata file in path {metadata_path}."
            

def find_directories(dirs):

    if not dirs: #default to cwd if no directories supplied
        click.echo("No directory paths supplied.  Searching for datasets in current working directory.")
        dirs = ['.']    
    found_dirs = set()
    for dir in dirs:
        found_dirs.update(x[0] for x in os.walk(pathlib.Path(dir).resolve()) \
            if (pathlib.Path(x[0]) / 'atbrepo.yaml').is_file() or \
                (pathlib.Path(x[0]) / 'atbrepo.yml').is_file()
                )
    if found_dirs:
        click.echo("Located datasets in the following paths:")
        click.echo("\n".join(found_dirs))
    else:
        click.secho("No datasets could be located in the supplied paths:", fg='red')
        click.echo("\n".join(str(pathlib.Path(dir).resolve()) for dir in dirs))
        sys.exit()            
    return found_dirs