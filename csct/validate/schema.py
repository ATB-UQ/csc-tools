import urllib.request
import urllib.error
import sys
import json

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
        #to-do: add tags, notes
    }
    return schema