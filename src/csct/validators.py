import os

import cerberus
import ckanapi.errors as errors

class ConfigValidator(cerberus.Validator):
    def _check_with_writable_directory(self, field, value):
        if not os.access(value, os.X_OK | os.W_OK):
            self._error(field, "not a writable directory")

    def _check_with_valid_authorization(self, field, _): 
        import csct.common, csct.remote
        from csct.config import get_config

        try:
            with csct.remote.Session(apikey=get_config('authorization')):
                pass
        except(errors.NotAuthorized):
             self._error(field, "invalid API token")
        except(errors.ValidationError):
            self._error(field, "validation error")
        except(errors.SearchError):
            self._error(field, "search error")
        except(errors.SearchIndexError):
            self._error(field, "search index error")
        except(errors.SearchQueryError):
            self._error(field, "search query error")
        except(errors.NotFound):
            self._error(field, "not found error")
        except:
            self._error(field, "unknown error while validating API token")

class MetadataValidator(cerberus.Validator):

    def _check_with_organization_list_for_site(self, field, value):

        import csct.remote
        from csct.config import get_config

        try:
            with csct.remote.Session(apikey=get_config('authorization')) as session:
                site_organizations = session.action.organization_list()
        except:
            self._error(field, "failed to retrieve organization list from server")

        if not value in site_organizations:
            self._error(field, f"unknown organization {value}") 

    def _check_with_organization_list_for_user(self, field, value):

        import csct.remote
        from csct.config import get_config

        try:
            with csct.remote.Session(apikey=get_config('authorization')) as session:
                raw_user_organizations = session.action.organization_list_for_user()
        except:
            self._error(field, "failed to retrieve organization list from server")

        user_organizations = [organization['name'] for organization in raw_user_organizations]

        if not value in user_organizations:
            self._error(field, f"authenticated user is not a member of {value}")  

    def _check_with_tag_allowed_characters(self, field, value):
        
        import re

        pattern = re.compile(r'^[a-zA-Z0-9 ._-]+$')

        if not pattern.match(value):
            self._error(value, "must contain only alphanumeric characters, spaces, hyphens, underscores, and dots")
        

class DirectoryValidator(cerberus.Validator):

    def _check_with_file(self, field, value):
        if not value == 'file':
            self._error(field, "must be a file")

    def _check_with_directory(self, field, value):
        if not value == 'directory':
            self._error(field, "must be a directory")

    def _validate_at_least_one_file(self, other, field, value):
        """
        Test if at least one file is present.

        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """
        if other not in self.document:
            self._error(field, f"invalid argument {other}")  
        if len(value) == 0 and len(self.document[other]) == 0:
            self._error(field, f"at least one {field} or {other} file is required")  
