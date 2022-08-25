import pathlib

import click
import yaml

from . import csct


@click.command(short_help="Upload datasets.")
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def upload(dirs):
    """
    Docstring.
    """
    config_path = pathlib.Path(csct.__path__[0]) / "csct_config.yaml"
    
    if config_path.is_file():
        try:
            with open(config_path, "r+") as c:
                config = yaml.safe_load(c)
        except:
            click.secho(f"Could not read configuration file in path {config}", fg='red')
    else:
        click.secho(f"Configuration file not found in path {config}", fg='red')

    found_dirs = csct.common.find_directories(dirs)

    for dir in found_dirs:
        if csct.validate.validate_single(True, True, True, True, dir):
            upload_single(config, dir)

def upload_single(config, dir):
    click.echo(f"Uploading dataset in path {dir}")
    print(config)

