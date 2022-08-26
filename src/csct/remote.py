import importlib.metadata

import ckanapi

import csct.common

class Session(ckanapi.RemoteCKAN):
    def __init__(self, address=csct.common.ckan_url, apikey=None, user_agent=f"csc_tools/{importlib.metadata.version('csc_tools')}", get_only=False, session=None, **kwargs):
        assert type(address) == str, "Address must be provided"
        super(Session, self).__init__(address, apikey=apikey, user_agent=user_agent, get_only=get_only, session=session)

        self.action.dashboard_activity_list() #TO-DO: change to more natural check in ckan 2.10 