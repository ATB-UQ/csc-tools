import importlib.metadata
import sys

import ckanapi
import click

import csct.common

class Session:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Session, cls).__new__(cls)
        return cls.instance

    def __enter__(self):
        from csct.config import get_config

        ua = f"csc_tools/{importlib.metadata.version('csc_tools')}"
        self.session = ckanapi.RemoteCKAN(csct.common.ckan_url, apikey=get_config('authorization'), user_agent=ua)
        try:
             with self.session as api:
                 api.action.get_site_user()
                 return self.session
        except ckanapi.errors.NotAuthorized:
            sys.exit()
        
    def __exit__(self, *_):
        self.session.close() 

session = Session()       