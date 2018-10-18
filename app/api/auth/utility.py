import jwt
import os

from datetime import datetime, timedelta

def generate_tokens(username,roles, first_login):
    """ A utility function to generate tokens for authorization.

    This function generates an access and refresh token given an accounts username.
    You can use and save both or discard one or the other as required.
    """

    access_token = jwt.encode(
        {
            'sub': 'authentication',
            'exp': datetime.utcnow() + timedelta(minutes=10),
            'username': username,
            'role': roles,
            'first_login': first_login
        },
        os.environ.get('APP_SECRET', 'sekkret'),
        algorithm='HS256'
    ).decode('utf-8')

    refresh_token = jwt.encode(
        {
            'sub': 'refresh',
            'exp': datetime.utcnow() + timedelta(days=7),
            'username': username,
            'role': roles,
            'first_login': first_login
        },
        os.environ.get('APP_SECRET', 'sekkret'),
        algorithm='HS256'
    ).decode('utf-8')

    return access_token, refresh_token
