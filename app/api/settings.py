import os

from dotenv import load_dotenv, find_dotenv

from app.api.resources.accounts import accounts
from app.api.resources.forms import forms
from app.api.resources.answers import answers

load_dotenv(find_dotenv())

config = {
    #'XML': False,
    'MONGO_HOST': os.environ.get('MONGO_HOST', 'localhost'),
    'MONGO_PORT': int(os.environ.get('MONGO_PORT', 27017)),
    'MONGO_USERNAME': os.environ.get('MONGO_USERNAME', ''),
    'MONGO_PASSWORD': os.environ.get('MONGO_PASSWORD', ''),
    'MONGO_DBNAME': os.environ.get('MONGO_DBNAME', 'api'),
    'AUTH_FIELD': 'user_id',
    'PUBLIC_RESOURCE_METHODS': ['GET'],
    'PUBLIC_ITEM_METHODS': ['GET'],
    'RESOURCE_METHODS': ['GET', 'POST'],
    'ITEM_METHODS': ['GET', 'PUT', 'DELETE'],
    'DOMAIN': {
        'accounts': accounts,
        'forms': forms,
        'answers': answers
    },
    'IF_MATCH': False,
    'X_DOMAINS': '*',
    'X_HEADERS': 'Authorization'
}
