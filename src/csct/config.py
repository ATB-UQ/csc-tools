import sys

import click
import yaml

@click.command(short_help="View and modify configuration options.")
@click.argument('name', nargs=1, required=False)
@click.argument('value', nargs=1, required=False)
@click.option('-l', '--list', is_flag=True, help="List all configuration variables and values.")
def config(list, name, value):
    """
    View and modify configuration options.

    \b
    NAME    Name of configuration variable.
    VALUE   Desired value of variable.
            [default: show current value of variable]
    """
    
    from csct.common import print_help

    if list and not (name or value):
        list_config()
    elif name and not value:
        list_config_single(name)
    else:
        print_help()

def list_config():
    """
    Print all configuration options.
    """

    configuration = get_config().items()  
    [click.echo(f"{key:<20}      {value}") for key, value in configuration]

def list_config_single(name):
    """
    Print the value of a single configuration option.
    """
    value = get_config(name) 
    click.echo(value)

def get_config(name=None):
    """
    Retrieve configuration options from configuration file.
    """

    from csct.common import config_path

    if config_path.is_file():
        try:
            with open(config_path, "r+") as config_file:
                configuration = yaml.safe_load(config_file)
        except:
            click.secho(f"Could not read configuration file in path {config_path}", fg='red')
            sys.exit()
        if not name:
            return configuration
        if name:
            return configuration[name]  
    else:
        click.secho(f"Configuration file not found in path {config_path}", fg='red')
        sys.exit()