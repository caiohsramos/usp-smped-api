import re

from eve.io.mongo import Validator

class MyValidator(Validator):
    def _validate_type_email(self, value):
        """
        Basic sanity check for emails, so at least we can prevent a bit of user
        error. Simply checks for an @ and a dot.
        """
        if re.match(r'[^@]+@[^@]+\.[^@]+', value):
            return True
        else:
            return self._error('Must be a valid e-mail')
