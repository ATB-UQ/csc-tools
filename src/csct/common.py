
import os
import pathlib
import sys

import click

ckan_url = 'https://molecular-dynamics.atb.uq.edu.au/'

print_width = 40

def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()

def find_directories(dirs):
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