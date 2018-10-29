from passlib.hash import pbkdf2_sha256
from flask import current_app as api, abort

accounts = {
    #'public_methods': [ 'POST' ],
    'public_item_methods': [ 'PATCH' ],
    'resource_methods': [ 'GET', 'POST' ],
    'item_methods': [ 'GET', 'PUT', 'PATCH', 'DELETE' ],
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username',
    },
    'allowed_roles': ['superuser', 'admin'],
    'schema': {
        'username': {
            'type': 'string',
            'minlength': 1,
            'required': True,
            'unique': True,
        },
        'password': {
            'type': 'string',
            'required': True,
            'default': ''
        },
        'email': {
            'type': 'email',
            'minlength': 3,
            'required': True,
            'unique': True,
        },
        'roles': {
            'type': 'list',
            'allowed': ['user', 'superuser', 'admin'],
            'required': True,
        },
        'access_token': { 'type': 'string', },
        'refresh_token': { 'type': 'string', },
        'first_login': { 'type':'boolean', 'default':True }
    },
    'datasource': {
        'projection': { 'password': 0, 'access_token': 0, 'refresh_token': 0, }, # Let's have some privacy, yes?
    }
}


def secure_account(account):
    """A utility function that secures accounts.

    It just generates a PBKDF2 encrypted password hash.
    """

    account['password'] = pbkdf2_sha256.encrypt(
        account['password'],
        rounds=20000,
        salt_size=16
    )

def secure_account_update(updates, original):
    if not original['first_login']:
        abort()
    else:
        updates['first_login'] = False
        updates['password'] = pbkdf2_sha256.encrypt(
            updates['password'],
            rounds=20000,
            salt_size=16
        )

def secure_accounts(accounts):
    for account in accounts:
        secure_account(account)

