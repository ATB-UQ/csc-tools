import sys
from . import config


def help():
    print("This is the help menu")   

def main():

    command = sys.argv[1]
    assert command in ['help', 'config'], \
        "Invalid command."
    args = sys.argv[2:]
    run_command(command, *args)
    

def run_command(command, *args):
    if command == 'help':
        help()
        
    elif command == 'config':
        config.run_config(*args)