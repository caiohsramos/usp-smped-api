import os
import jwt

from passlib.hash import pbkdf2_sha256
from flask import Blueprint, abort, request, make_response, current_app, jsonify, current_app as api
from datetime import timedelta
from functools import update_wrapper

from api.auth.utility import generate_tokens

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

TokenService = Blueprint('TokenService', __name__)

@TokenService.route('/tokens', methods=['POST','OPTIONS'])
@crossdomain(origin='*')
def issue_tokens():
    data = request.get_json()
    accounts = api.data.driver.db['accounts']
    account = accounts.find_one({ 'username': data['username'] })

    if account and pbkdf2_sha256.verify(data['password'], account['password']):
        if account['username'] == 'admin':
            return jsonify({
                'access_token': account['access_token'],
                'refresh_token': account['refresh_token']
            })

        access_token, refresh_token = generate_tokens(account['username'],account['roles'],account['first_login'])

        account['access_token'] = access_token
        account['refresh_token'] = refresh_token
        query = {}
        query['_id'] = account['_id']
        accounts.replace_one(query,account)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
        })
    else:
        abort(401, description="The provided credentials are incorrect.")


@TokenService.route('/refresh', methods=['POST','OPTIONS'])
@crossdomain(origin='*')
def refresh_token():
    data = request.get_json()
    accounts = api.data.driver.db['accounts']
    account = accounts.find_one({ 'refresh_token': data['refresh_token'] })

    if not account:
        abort(401, description="The provided refresh token is invalid")

    try:
        if account['username'] == 'admin':
            return jsonify({
                'access_token': account['access_token']
            })

        #generate exception if refresh_token expired
        jwt.decode(data['refresh_token'], os.environ.get('APP_SECRET', 'sekkret'), algorithms=['HS256'])
        
        access_token, _ = generate_tokens(account['username'],account['roles'],account['first_login'])

        account['access_token'] = access_token
        query = {}
        query['_id'] = account['_id']
        accounts.replace_one(query,account)

        return jsonify({
            'access_token': access_token,
        })
         
    except jwt.ExpiredSignatureError:
        abort(401, description="The refresh token is expired.")
