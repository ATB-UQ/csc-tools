import os
from pathlib import Path
import click
import yaml
from .schema import raw_metadata_schema

def find_directories(dirs):
    found_dirs = set()
    for dir in dirs:
        found_dirs.update(x[0] for x in os.walk(dir) \
            if (Path(x[0]) / 'atbrepo.yaml').is_file() or \
                (Path(x[0]) / 'atbrepo.yml').is_file() or \
                (Path(x[0]) / 'metadata.yaml').is_file() or \
                (Path(x[0]) / 'metadata.yml').is_file()
                )
    return found_dirs

def validate_metadata(dirs, raw_metadata_schema):
    metadata_schema = yaml.safe_load(raw_metadata_schema)

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

    validate_metadata(found_dirs, raw_metadata_schema)    