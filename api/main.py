import json

import certifi as certifi
import requests as requests
import urllib3 as urllib3
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_restful import Api

from PostgresStorage import PostgresStorage
from db.dao import RemainingLikesDao
from db.models import User
from errors.AuthorizationError import AuthorizationError
from utilities.Logs import Logs
from utilities.Results import Results

storage_session = PostgresStorage()
app = Flask(__name__)
CORS(app)
api = Api(app)


def get_liked_value(value: str or None) -> bool or None:
    if value is not None:
        return True if value == '1' else False
    return None


def get_headers() -> dict:
    return {'X-Auth-Token': storage_session.get_api_key(), 'Host': storage_session.get_base_url()}


def make_api_call_request(url: str, method: str):
    pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    return pool_manager.request(method=method, url=url, headers=get_headers())


def get_remaining_likes() -> int:
    url: str = 'https://%s/v2/profile?include=likes' % storage_session.get_base_url()
    like_request = make_api_call_request(url=url, method='GET')
    if like_request.status == requests.status_codes.codes.unauthorized:
        raise AuthorizationError(message='while trying to retrieve remaining likes')
    data = json.loads(like_request.data.decode('utf-8'))
    if 'data' in data:
        return data['data']['likes']['likes_remaining']
    return 0


@app.route('/api/users', methods=['GET'])
def get_users():
    page: int = 1
    page_size: int = 10
    liked: bool or None = None
    try:
        page = int(request.args.get('page', default=1))
        page_size = int(request.args.get('size', default=10))
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
    size: int = 10
    liked: bool or None = None
    try:
        page = int(request.args.get('page', default=1))
        size = int(request.args.get('size', default=10))
        liked = get_liked_value(request.args.get('liked'))
    except ValueError:
        pass
    return make_response(jsonify({
        'users': storage_session.search_users(name_partial=name, page=page, size=size, liked=liked),
        'total': storage_session.fetch_filtered_users_count(name_partial=name)
    }))


@app.route('/api/users/like/<int:user_id>', methods=['POST'])
def like_user(user_id: int):
    try:
        if get_remaining_likes() < 1:
            return make_response(jsonify({
                'message': 'No more likes available',
            }), requests.status_codes.codes.bad_request)
    except AuthorizationError as e:
        return make_response(jsonify({
            'message': e.message,
        }), requests.status_codes.codes.unauthorized)
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
        url: str = 'https://%s/like/%s' % (storage_session.get_base_url(), user.user_id)
        pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        like_request = pool_manager.request(method='POST', url=url, headers=get_headers(), body=json.dumps({
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
    return make_response(jsonify({
        'logs': [log.to_dict() for log in Logs(storage=storage_session).get_logs_chunk()],
    }), requests.status_codes.codes.ok)


@app.route('/api/logs/archive', methods=['GET'])
def get_archive_logs():
    logs: list[dict] = []
    try:
        from_log = request.args.get('from')
        if from_log is not None:
            logs = [log.to_dict() for log in Logs(storage=storage_session).get_archive_logs(from_log=int(from_log))]
    except ValueError:
        pass
    return make_response(jsonify({'logs': logs}), requests.status_codes.codes.ok)


@app.route('/api/logs/tail', methods=['GET'])
def get_tail_logs():
    logs: list[dict] = []
    try:
        to_log = request.args.get('to')
        if to_log is not None:
            logs = [log.to_dict() for log in Logs(storage=storage_session).get_latest_logs(to_log=int(to_log))]
    except ValueError:
        pass
    return make_response(jsonify({'logs': logs}), requests.status_codes.codes.ok)


@app.route('/api/logs/search', methods=['GET'])
def search_logs():
    try:
        criteria = request.args.get('search')
        if criteria is not None:
            return make_response(jsonify({
                'logs': [log.to_dict() for log in Logs(storage=storage_session).search_logs(criteria=criteria)]
            }), requests.status_codes.codes.ok)
    except ValueError:
        pass
    return make_response(jsonify({'logs': []}), requests.status_codes.codes.ok)


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
    url: str = 'https://%s/v2/profile?include=likes' % storage_session.get_base_url()
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
