import urllib.request
import urllib.error
import sys
import json
from .common import *

def get_config_schema():
    pass

def get_metadata_schema():

    #pull list of valid organizations from CKAN API on the web
    orgs_web_location = 'api/3/action/organization_list'
    orgs_url = urllib.parse.urljoin(ckan_url, orgs_web_location)

    try: 
        with urllib.request.urlopen(orgs_url) as url:
            organizations = json.loads(url.read().decode())['result']
    except urllib.error.URLError:
        sys.exit("Could not retrieve organization list from server (" + ckan_url + ").  Please try again later.")

    schema = {
        'title': {
            'type': 'string',
            'required': True,
            'empty': False,
        },
        # 'author': {
        #     'type': 'string',
        #     'required': True,
        #     'empty': False,
        # },
        # 'author_email': {
        #     'type': 'string',
        #     'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        #     'required': True,
        #     'empty': False,
        # },
        'organization': {
            'allowed': organizations,
            'required': True,
            'empty': False,
        },
        'program': {
            'type': 'string',
            'allowed': ['AMBER', 'GROMOS', 'GROMACS'],
            'required': True,
            'empty': False,
        },
        'private': {
            'allowed': [True, False],
        },
        'notes': {
            'type': 'string',
            'required': True,
            'empty': False,
        },
        'tags': {
            'type': 'list',
            'schema': {'type': 'string'},
            'required': True,
            'empty': False,
        },
    }
    return schema

def get_directory_structure_schema():

    schema = {
        'control': {
            'type': 'string',
            'required': True,
            'empty': False,
            'check_with': 'directory',
        },
        'energy': {
            'type': 'string',
            'required': True,
            'empty': False,
            'check_with': 'directory',
        },
        'final-coordinates': {
            'type': 'string',
            'required': True,
            'empty': False,
            'check_with': 'directory',
        },
        'input-coordinates': {
            'type': 'string',
            'required': True,
            'empty': False,
            'check_with': 'directory',
        },
        'log': {
            'type': 'string',
            'required': True,
            'empty': False,
            'check_with': 'directory',
        },
        'reference-coordinates': {
            'type': 'string',
            'required': True,
            'empty': False,
            'check_with': 'directory',
        },
        'topology': {
            'type': 'string',
            'required': True,
            'empty': False,
            'check_with': 'directory',
        },
        'trajectory': {
            'type': 'string',
            'required': True,
            'empty': False,
            'check_with': 'directory',
        },
    }    
    return schema

def get_directory_contents_schema():

    schema = {
        'control': {
            'type': 'dict',
            'required': True,
            'empty': True,
            'at_least_one_file': 'log',
        },
        'energy': {
            'type': 'dict',
            'required': True,
            'empty': True,
        },
        'final-coordinates': {
            'type': 'dict',
            'required': True,
            'empty': True,
        },
        'input-coordinates': {
            'type': 'dict',
            'required': True,
            'empty': False,
        },
        'log': {
            'type': 'dict',
            'required': True,
            'empty': True,
            'at_least_one_file': 'control',
        },
        'reference-coordinates': {
            'type': 'dict',
            'required': True,
            'empty': True,
        },
        'topology': {
            'type': 'dict',
            'required': True,
            'empty': False,
        },
        'trajectory': {
            'type': 'dict',
            'required': True,
            'empty': True,
        },
    }    
    return schema