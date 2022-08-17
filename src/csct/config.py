import os
import yaml

import sys
#sys.setrecursionlimit(24)

def locate(config_dir):
    config_path = os.path.join(config_dir,"csct_config.yml")

    if os.path.isfile(config_path):
        #to-do: enforce schema with cerberus
        with open (config_path, "r+") as c:
            config = yaml.safe_load(c)
            return(config_path)
    elif config_dir == os.path.dirname(config_dir): #if the parent directory is the same as the current directory (i.e., if we are at the top level)
        sys.exit("Could not locate csct_config.yml in the specified directory or any parent directories.")
    else:
        locate(os.path.dirname(config_dir))

def list(config_path, args):
    print("Reading configuration file from {location}\n".format(location=config_path))
    print("Current configuration settings:")
    
def run_config(command, args):
    
    #begin the search for the config file in the cwd
    config_dir = os.getcwd()

    if command == 'locate':
        config_path = locate(config_dir)
        print("Located configuration file in {location}".format(location=config_path))

    if command == 'list':
        config_path = locate(config_dir)
        list(config_path, args)
    else:
        command.print_help()
        sys.exit() #if I remove this, it prints the namespace object?