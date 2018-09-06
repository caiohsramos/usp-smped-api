import os
import jwt

from eve import Eve
from eve.auth import TokenAuth
from flask import abort, current_app as api

class MyAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        """ Checks for the validity of the provided JWT and grants access.

        First we check to see if any user with a given token exists. If it does,
        we decode the token and check if the payload is verifiable. If so, we're
        good to go. If not, we abort with 401 unauthorized.
        """

        accounts = api.data.driver.db['accounts']
        lookup = { 'access_token': token }
        if allowed_roles:
            # only retrieve a user if his roles match ``allowed_roles``
            lookup['roles'] = {'$in': allowed_roles}
        account = accounts.find_one(lookup)

        if not account:
            abort(401, description="The provided access token is invalid or role no allowed")

        try:
            access_payload = jwt.decode(token, os.environ.get('APP_SECRET', 'sekkret'), algorithms=['HS256'])

            return account and account['username'] == access_payload['username']
        except jwt.ExpiredSignatureError:
            abort(401, description="Your access token is expired.")
