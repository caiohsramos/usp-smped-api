import os
import jwt

from passlib.hash import pbkdf2_sha256
from flask import Blueprint, abort, request, jsonify, current_app as api

from api.auth.utility import generate_tokens

TokenService = Blueprint('TokenService', __name__)

@TokenService.route('/tokens', methods=['POST'])
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

        access_token, refresh_token = generate_tokens(account['username'],account['roles'])

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


@TokenService.route('/refresh', methods=['POST'])
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
        
        access_token, _ = generate_tokens(account['username'],account['roles'])

        account['access_token'] = access_token
        query = {}
        query['_id'] = account['_id']
        accounts.replace_one(query,account)

        return jsonify({
            'access_token': access_token,
        })
    except jwt.ExpiredSignatureError:
        abort(401, description="The refresh token is expired.")
