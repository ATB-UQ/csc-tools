import urllib.request
import urllib.error
import sys
import json
import cerberus

def get_metadata_schema():

    #pull list of valid organizations from CKAN API on the web
    ckan_url = 'https://molecular-dynamics.atb.uq.edu.au/'
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

class DirectoryValidator(cerberus.Validator):

    def _check_with_not_duplicate(self, field, value):
        if value == 'duplicate':
            self._error(field, "only one metadata file must be present")

    def _check_with_file(self, field, value):
        if not value == 'file':
            self._error(field, "must be a file")

    def _check_with_directory(self, field, value):
        if not value == 'directory':
            self._error(field, "must be a directory")        

def get_directory_schema():

    schema = {
        'control': {
            'type': 'string',
            'check_with': 'directory',
            'required': True,
            'empty': False,
        },
        'energy': {
            'type': 'string',
            'check_with': 'directory',
            'required': True,
            'empty': False,
        },
        'final-coordinates': {
            'type': 'string',
            'check_with': 'directory',
            'required': True,
            'empty': False,
        },
        'input-coordinates': {
            'type': 'string',
            'check_with': 'directory',
            'required': True,
            'empty': False,
        },
        'log': {
            'type': 'string',
            'check_with': 'directory',
            'required': True,
            'empty': False,
        },
        'reference-coordinates': {
            'type': 'string',
            'check_with': 'directory',
            'required': True,
            'empty': False,
        },
        'topology': {
            'type': 'string',
            'check_with': 'directory',
            'required': True,
            'empty': False,
        },
        'trajectory': {
            'type': 'string',
            'check_with': 'directory',
            'required': True,
            'empty': False,
        },
    }    
    return schema