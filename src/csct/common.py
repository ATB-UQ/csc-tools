from pathlib import Path
import os
import sys
import click

global ckan_url
ckan_url = 'https://molecular-dynamics.atb.uq.edu.au/'

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

