import sys
from os import path, listdir, symlink, makedirs, readlink, getcwd #imports from os
import warnings
import argparse
import urllib.request
from urllib.parse import urljoin
from urllib.error import URLError
import json
import yaml

trajectory_data_path = ""

#pull list of valid organizations from CKAN API on the web
ckan_url = 'https://molecular-dynamics.atb.uq.edu.au/'
orgs_web_location = 'api/3/action/organization_list'
orgs_url = urljoin(ckan_url, orgs_web_location)

try: 
    with urllib.request.urlopen(orgs_url) as url:
        organizations = json.loads(url.read().decode())['result']
        print(organizations)
except URLError:
    sys.exit("Could not retrieve organization list from ACSC server (" + ckan_url + ").  Please try again later.")
#organizations = ["bernhardt", "chalmers", "deplazes", "krenske", "malde", "mduq", "omara", "smith", "yu"]
#programs we support parsing for right now
programs = "AMBER", "GROMOS", "GROMACS"

def validate_metadata( #function definition for function that returns dataset control parameters with arguments: 
    dataset_path, #path of the dataset
):
    config_path = path.join(dataset_path, "metadata.yml") #check for this name first
    
    if not path.exists(config_path): #if it's not there...
        config_path = path.join(dataset_path, "atbrepo.yml") #check for the alternative name

    if not path.exists(config_path): #if it's still not there...
        raw_config = {} #define an empty dictionary with no keys
    else: #if the path to the metadata file exists
        try: 
            with open(config_path, "r") as c: #try to open the metadata file
                raw_config = yaml.safe_load(c) #if the metadata file is there, create the raw_config dictionary by loading the yaml file
        except FileNotFoundError: 
            raise Exception("Exception: could not locate metadata file.") #throw exception if it's not there
    USE_KEYS = ("title", "notes", "author", "author_email", "program", "private", "organization") #list of keys to use to look up in the metadata dictionary (raw_config)
    config = { #dictionary of the metadata
        key:raw_config[key] \
            for key in raw_config if key in USE_KEYS
    }

    if 'title' in config and config['title'] != None: #if there is a title field and the value is not null
        title = config['title']
    else: 
        warnings.warn("No title specified in metadata file. Defaulting to dataset basename.")       
        title = dataset            
    print("Title: " + title)

    try: 
        author = config['author']
    except (KeyError, ValueError):
        warnings.warn("No author specified in metadata file.")       
        title = dataset
    print("Title: " + title)

    if not (('author' in config) or config['author']):
        raise Exception("Exception: no author specified in metadata file.")
    else:
        print("Author: " + config['author'])    

    if not (('author_email' in config) or config['author_email']):
        raise Exception("Exception: no author e-mail address specified in metadata file.")
    else:
        print("Author E-mail Address: " + config['author_email'])

    if not (('organization' in config) or config['organization']):
        raise Exception("Exception: no organization specified in metadata file.")
    elif not config['organization'].lower() in organizations:
        raise Exception("Exception: invalid organization specified in metadata file. Valid organizations are: {}".format(", ".join(organizations)))
    else:
        organization = config['organization'].lower()
        print("Organization: " + organization)     

    if not (('program' in config) or config['program']):
       raise Exception("Exception: no simulation program specified in metadata file.") 
    elif all(x != config['program'] for x in programs):
        raise Exception("Exception: invalid program specified in metadata file.")
    else:
        print("Program: " + config['program'])

    if not (('private' in config) or config['private']):
        warnings.warn("Warning: dataset privacy level not specified. Defaulting to public.")
        config['private'] = "False"
    print("Private:" + config['private'])

    try:
        tags = [dict(name=tag) for tag in raw_config["tags"] ] #creates a list of dictionaries of form {name=tag}
    except KeyError:
        warnings.warn("Warning: no tags supplied.")
        tags = [] #If missing tags, just has none
   #special_tags = raw_config["special_tags"]
   #for tag_type in special_tags:
   #    tags.append( dict(name=special_tags[tag_type], vocabulary_id=tag_type) )

    return config, tags

parser = argparse.ArgumentParser() #create an argument parser object
parser.add_argument( #add an argument for specifying a specific directory
    "-d", "--dir", #argument provided by typing either of these
    default="", #defaults to no directory
    help="Specify the full path to a directory containing a dataset to validate", #help for the argument
)

args = parser.parse_args() #parse the arguments supplied and save as a namespace object

if args.dir == "": #if the argument namespace is empty...
    dataset_path = getcwd()
    dataset_basename = path.basename(dataset_path)
else:
    if not path.isdir(args.dir): #if the path supplied by the -d argument is not a directory...
        sys.stderr.write("Path is not a directory: " + args.dir + "\n") #write to standard error
        exit(1) #we consider this to be a fatal error, program exits
    dataset_path = path.relpath(args.dir, trajectory_data_path)
    dataset_basename = path.basename(args.dir)    
dataset_config(dataset_basename,dataset_path,trajectory_data_path)    

def validate(dataset_path):
    parse_metadata(dataset_path)

def cmd_validate(args=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=float)
    parsed_args = parser.parse_args(args)

    print(metadata_summary(parsed_args.dir))