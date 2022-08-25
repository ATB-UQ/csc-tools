import cerberus

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
            return False   
        if len(value) == 0 and len(self.document[other]) == 0:
            self._error(field, f"at least one {field} or {other} file is required")  