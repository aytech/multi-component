import json
import os
from typing import Optional

import certifi as certifi
import requests as requests
import urllib3 as urllib3
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_restful import Api

from PostgresStorage import PostgresStorage
from db.dao import RemainingLikesDao
from db.models import User, Log
from utilities.Results import Results

storage_session = PostgresStorage()
app = Flask(__name__)
CORS(app)
api = Api(app)

PAGE_SIZE: int = int(os.environ.get('PAGE_SIZE', default=10))
AUTH_TOKEN: str = os.environ.get('AUTH_TOKEN')
BASE_URL: str = os.environ.get('BASE_URL')


def get_liked_value(value: str or None) -> bool or None:
    if value is not None:
        return True if value == '1' else False
    return None


def make_api_call_request(url: str, method: str):
    request_headers = {'X-Auth-Token': AUTH_TOKEN, 'Host': BASE_URL}
    pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    return pool_manager.request(method=method, url=url, headers=request_headers)


def get_remaining_likes() -> int:
    url: str = 'https://%s/v2/profile?include=likes' % BASE_URL
    like_request = make_api_call_request(url=url, method='GET')
    data = json.loads(like_request.data.decode('utf-8'))
    if 'data' in data:
        return data['data']['likes']['likes_remaining']
    return 0


@app.route('/api/users', methods=['GET'])
def get_users():
    page: int = 1
    page_size: int = PAGE_SIZE
    liked: bool or None = None
    try:
        page = int(request.args.get('page', default=1))
        page_size = int(request.args.get('size', default=PAGE_SIZE))
        liked = get_liked_value(request.args.get('liked'))
    except ValueError:
        pass
    return make_response(jsonify({
        'users': storage_session.list_users(page=page, page_size=page_size, liked=liked),
        'total': storage_session.fetch_all_users_count()
    }))


@app.route('/api/users/search/<string:name>', methods=['GET'])
def search_users(name: str):
    page: int = 1
    size: int = PAGE_SIZE
    liked: bool or None = None
    try:
        page = int(request.args.get('page', default=1))
        size = int(request.args.get('size', default=PAGE_SIZE))
        liked = get_liked_value(request.args.get('liked'))
    except ValueError:
        pass
    return make_response(jsonify({
        'users': storage_session.search_users(name_partial=name, page=page, size=size, liked=liked),
        'total': storage_session.fetch_filtered_users_count(name_partial=name)
    }))


@app.route('/api/users/like/<int:user_id>', methods=['POST'])
def like_user(user_id: int):
    if get_remaining_likes() < 1:
        return make_response(jsonify({
            'message': 'No more likes available',
        }), requests.status_codes.codes.bad_request)
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
    deleted_user: User = storage_session.delete_user_by_id(user_id=user_id)
    return make_response(jsonify({
        'message': 'User %s deleted' % deleted_user.name
    }), requests.status_codes.codes.ok)


@app.route('/api/logs', methods=['GET'])
def get_logs():
    from_index: Optional[int] = None
    limit: int = 100
    try:
        from_index_arg = request.args.get('from')
        if from_index_arg is not None:
            from_index = int(from_index_arg)
        limit = int(request.args.get('limit', default=100))
    except ValueError:
        pass
    logs: list[Log] = storage_session.get_logs(limit=limit, from_index=from_index)
    return make_response(jsonify({
        'logs': [log.to_dict() for log in logs],
        'last': True if len(logs) == 0 else storage_session.is_last_log(log_id=logs[0].id)
    }), requests.status_codes.codes.ok)


@app.route('/api/settings/token/<string:token>', methods=['POST'])
def add_or_update_token(token: str):
    storage_session.add_update_api_key(key_value=token)
    return make_response(jsonify({
        'updated': True,
    }), requests.status_codes.codes.ok)


@app.route('/api/settings/url/<string:url>', methods=['POST'])
def add_or_update_base_url(url: str):
    storage_session.add_update_base_url(url_value=url)
    return make_response(jsonify({
        'updated': True,
    }), requests.status_codes.codes.ok)


@app.route('/api/settings', methods=['GET'])
def get_settings():
    return make_response(jsonify({
        'api_key': storage_session.get_api_key(),
        'base_url': storage_session.get_base_url(),
        'teasers': storage_session.get_teasers(),
    }), requests.status_codes.codes.ok)


@app.route('/api/settings/likes', methods=['GET'])
def get_likes_remaining():
    url: str = 'https://%s/v2/profile?include=likes' % BASE_URL
    response = make_api_call_request(url=url, method='GET')
    if response.status == requests.status_codes.codes.unauthorized:
        return make_response(jsonify({
            'message': 'Unauthorized',
        }), requests.status_codes.codes.unauthorized)
    if response.status == requests.status_codes.codes.forbidden:
        return make_response(jsonify({
            'message': 'Forbidden',
        }), requests.status_codes.codes.forbidden)
    likes: RemainingLikesDao = Results.remaining_likes(json_data=json.loads(response.data.decode('utf-8')))
    return make_response(jsonify(likes.to_dict()), requests.status_codes.codes.ok)


if __name__ == '__main__':
    app.run(debug=True)
