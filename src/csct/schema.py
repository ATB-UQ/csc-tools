import json
import urllib.error, urllib.request
import sys

import ckanapi
import click

import csct

def get_config_schema():

    schema = {
        'authorization': {
            'check_with': 'valid_authorization',
            'empty': False,
            'required': True,
            'type': 'string',
        },
    }
    return schema

def get_metadata_schema():

    #pull list of valid organizations from CKAN API on the web
    # orgs_web_location = 'api/3/action/organization_list'
    # orgs_url = urllib.parse.urljoin(csct.common.ckan_url, orgs_web_location)

    # try:
    #     with urllib.request.urlopen(orgs_url) as url:
    #         organizations = json.loads(url.read().decode())['result']
    # except urllib.error.URLError:
    #     click.secho("FAILED", fg='red')
    #     click.secho(f"Could not retrieve organization list from {csct.common.ckan_url}.", fg='red')
    #     sys.exit()

    schema = {
        'title': {
            'empty': False,
            'required': True,
            'type': 'string',
        },
        # 'author': {
        #     'empty': False,
        #     'required': True,
        #     'type': 'string',
        # },
        # 'author_email': {
        #     'empty': False,
        #     'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        #     'required': True,
        #     'type': 'string',
        # },
        'organization': {
            'check_with': ('organization_list_for_user', 'organization_list_for_site'),
            'empty': False,
            'required': True,
            'type': 'string',
        },
        'program': {
            'allowed': ['AMBER', 'GROMOS', 'GROMACS'],
            'empty': False,
            'required': True,            
            'type': 'string',
        },
        'private': {
            'allowed': [True, False],
        },
        'notes': {
            'empty': False,
            'required': True, 
            'type': 'string',
        },
        'tags': {
            'empty': False,
            'required': True,            
            'schema': {'type': 'string'},            
            'type': 'list',
        },
    }
    return schema

def get_directory_structure_schema():

    schema = {
        'control': {
            'check_with': 'directory',
            'empty': False,
            'required': True,
            'type': 'string',
        },
        'energy': {
            'check_with': 'directory',
            'empty': False,
            'required': True,
            'type': 'string',
        },
        'final-coordinates': {
            'check_with': 'directory',
            'empty': False,
            'required': True,
            'type': 'string',
        },
        'input-coordinates': {
            'check_with': 'directory',
            'empty': False,
            'required': True,
            'type': 'string',
        },
        'log': {
            'check_with': 'directory',
            'empty': False,
            'required': True,
            'type': 'string',
        },
        'reference-coordinates': {
            'check_with': 'directory',
            'empty': False,
            'required': True,
            'type': 'string',
        },
        'topology': {
            'check_with': 'directory',
            'empty': False,
            'required': True,
            'type': 'string',
        },
        'trajectory': {
            'check_with': 'directory',
            'empty': False,
            'required': True,
            'type': 'string',
        },
    }    
    return schema

def get_directory_contents_schema():

    schema = {
        'control': {
            'at_least_one_file': 'log',
            'empty': True,
            'required': True,
            'type': 'dict',
        },
        'energy': {
            'empty': True,
            'required': True,
            'type': 'dict',
        },
        'final-coordinates': {
            'empty': True,
            'required': True,
            'type': 'dict',
        },
        'input-coordinates': {
            'empty': False,
            'required': True,
            'type': 'dict',
        },
        'log': {
            'at_least_one_file': 'control',
            'empty': True,
            'required': True,
            'type': 'dict',
        },
        'reference-coordinates': {
            'empty': True,
            'required': True,
            'type': 'dict',
        },
        'topology': {
            'empty': False,
            'required': True,
            'type': 'dict',
        },
        'trajectory': {
            'empty': True,
            'required': True,
            'type': 'dict',
        },
    }    
    return schema