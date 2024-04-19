import click

@click.command(short_help="View and edit dataset metadata.")
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False))
@click.option('-a', '--all', is_flag=True, help="Validate all dataset properties. [default]")
@click.option('-e', '--export', is_flag=True, help="Validate all dataset properties and attempt to export dataset.")
@click.option('-c', '--config', is_flag=True, help="Validate configuration settings.")
@click.option('-m', '--metadata', is_flag=True, help="Validate configuration settings and dataset metadata.")
@click.option('-s', '--structure', is_flag=True, help="Validate dataset subdirectory structure.")
@click.option('-f', '--files', is_flag=True, help="Validate dataset subdirectory structure and files.")
def metadata(add, remove, replace, view, dirs):
    """
    View and modify metadata.

    \b
    DIRS    Directories to recursively scan for datasets. 
            [default: current working directory]
    """
    pass