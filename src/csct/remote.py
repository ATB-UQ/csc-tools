import importlib.metadata
import sys

import ckanapi
import click

import csct.common

class Session(ckanapi.RemoteCKAN):

    def __init__(self, address=csct.common.ckan_url, apikey=None, get_only=False, session=None, **kwargs):
        self.ua = f"csc_tools/{importlib.metadata.version('csc_tools')}"
        assert type(address) == str, "Address must be provided"
        super(Session, self).__init__(address, apikey=apikey, user_agent=self.ua, get_only=get_only, session=session)

        # try:
        #      with self.session as api:
        #          api.action.dashboard_activity_list() #TO-DO: change to more natural check in ckan 2.10
        #          return self.session
        # except ckanapi.errors.NotAuthorized:
        #     sys.exit()
    


#session = Session(**config_dict)       