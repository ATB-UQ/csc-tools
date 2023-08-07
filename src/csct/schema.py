def get_config_schema():

    schema = {
        'authorization': {
            'check_with': 'valid_authorization',
            'empty': False,
            'required': True,
            'type': 'string',
        },
        'export_path': {
            'check_with': 'writable_directory',
            'empty': False,
            'required': True,
            'type': 'string',
        },
    }
    return schema

def get_metadata_schema():

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
            'allowed': ['AMBER', 'CHARMM', 'GROMACS', 'GROMOS', 'NAMD'],
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
        'forcefield-files': {
            'check_with': 'directory',
            'empty': False,
            'required': False,
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
        'miscellaneous': {
            'check_with': 'directory',
            'empty': False,
            'required': False,
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
        'forcefield-files': {
            'empty': True,
            'required': False,
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
        'miscellaneous': {
            'empty': True,
            'required': False,
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