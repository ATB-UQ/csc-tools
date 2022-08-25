import click

import csct.common, csct.config, csct.validate

@click.command(short_help="Upload datasets.")
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
def upload(dirs):
    """
    Docstring.
    """
    config = csct.config.get_config()

    found_dirs = csct.common.find_directories(dirs)

    for dir in found_dirs:
        if csct.validate.validate_single(True, True, True, True, dir):
            upload_single(config, dir)

def upload_single(config, dir):
    click.echo(f"Uploading dataset in path {dir}")
    print(config)