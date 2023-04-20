import json
import os

import certifi as certifi
import requests as requests
import urllib3 as urllib3
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_restful import Api

from PostgresStorage import PostgresStorage
from models import User

storage_session = PostgresStorage()
app = Flask(__name__)
CORS(app)
api = Api(app)

PAGE_SIZE: int = int(os.environ.get('PAGE_SIZE', default=10))
AUTH_TOKEN: str = os.environ.get('AUTH_TOKEN')
BASE_URL: str = os.environ.get('BASE_URL')


@app.route('/api/users', methods=['GET'])
def get_users():
    page: int = 1
    page_size: int = PAGE_SIZE
    try:
        page = int(request.args.get('page', default=1))
        page_size = int(request.args.get('size', default=PAGE_SIZE))
    except ValueError:
        pass
    return make_response(jsonify({
        'users': storage_session.list_users(page=page, page_size=page_size),
        'total': storage_session.fetch_all_users_count()
    }))


@app.route('/api/users/search/<string:name>', methods=['GET'])
def search_users(name: str):
    page: int = 1
    page_size: int = PAGE_SIZE
    try:
        page = int(request.args.get('page', default=1))
        page_size = int(request.args.get('size', default=PAGE_SIZE))
    except ValueError:
        pass
    return make_response(jsonify({
        'users': storage_session.search_users(name_partial=name, page=page, page_size=page_size),
        'total': storage_session.fetch_filtered_users_count(name_partial=name)
    }))


@app.route('/api/users/like/<int:user_id>', methods=['POST'])
def like_user(user_id: int):
    pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    request_headers = {'X-Auth-Token': AUTH_TOKEN, 'Host': BASE_URL}
    user: User = storage_session.fetch_user_by_id(user_id=user_id)
    if user is None:
        return make_response(jsonify({
            'message': 'User not found'
        }), requests.status_codes.codes.bad_request)
    elif len(user.photos) < 1:
        return make_response(jsonify({
            'message': 'User has no photos'
        }), requests.status_codes.codes.bad_request)
    else:
        url: str = 'https://%s/like/%s' % (BASE_URL, user.user_id)
        like_request = pool_manager.request(method='POST', url=url, headers=request_headers, body=json.dumps({
            's_number': user.s_number,
            'liked_content_id': user.photos[0].photo_id,
            'liked_content_type': 'photo'
        }))
        if like_request.status == requests.status_codes.codes.ok:
            user.liked = True
            storage_session.update_user(user=user)

        return make_response(jsonify({
            'message': like_request.msg,
            'reason': like_request.reason
        }), like_request.status)


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    storage_session.delete_user_by_id(user_id=user_id)
    return make_response(jsonify({
        'message': 'User deleted'
    }), requests.status_codes.codes.ok)


if __name__ == '__main__':
    app.run(debug=True)
