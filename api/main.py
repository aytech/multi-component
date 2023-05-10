import json
import os
import grpc
from typing import Optional

import requests as requests
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_restful import Api
from google.protobuf.json_format import MessageToJson

import protos.profiles_pb2_grpc
from protos.profiles_pb2 import ProfilesRequest, ProfilesSearchRequest
from PostgresStorage import PostgresStorage
from db.dao import RemainingLikesDao, UserDao
from db.models import User
from routes import app_routes
from utilities.Logs import Logs
from utilities.Request import Request
from utilities.Results import Results

grpc_host: str = os.environ.get('GRPC_HOST', default='localhost')
grpc_port: str = os.environ.get('GRPC_PORT', default='50051')

storage_session: PostgresStorage = PostgresStorage()
app_request: Request = Request(storage=storage_session)
app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route(app_routes['LIST_USERS'], methods=['GET'])
def get_users():
    page: int = 1
    page_size: int = 10
    status: Optional[str] = None
    try:
        page = int(request.args.get('page', default=1))
        page_size = int(request.args.get('size', default=10))
        status = request.args.get('status')
    except ValueError:
        pass
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = protos.profiles_pb2_grpc.ConnectorStub(channel=channel)
        response = stub.FetchProfiles(ProfilesRequest(status=status, page=page, page_size=page_size))
        return make_response(MessageToJson(response.reply), requests.status_codes.codes.ok)


@app.route(app_routes['SEARCH_USERS'], methods=['GET'])
def search_users(name: str):
    page: int = 1
    size: int = 10
    status: Optional[str] = None
    try:
        page = int(request.args.get('page', default=1))
        size = int(request.args.get('size', default=10))
        status = request.args.get('status')
    except ValueError:
        pass
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = protos.profiles_pb2_grpc.ConnectorStub(channel=channel)
        response = stub.SearchProfiles(ProfilesSearchRequest(value=name, status=status, page=page, page_size=size))
        return make_response(MessageToJson(response.reply), requests.status_codes.codes.ok)


@app.route(app_routes['LIKE_USER'], methods=['POST'])
def like_user(user_id: int):
    result: Optional[User] = storage_session.schedule_like(user_id=user_id)
    status = requests.status_codes.codes.ok if result is not None else requests.status_codes.codes.bad_request
    return make_response(jsonify({
        'message': 'User scheduled for like' if result is not None else 'User already scheduled or liked'
    }), status)


@app.route(app_routes['DISLIKE_USER'], methods=['POST'])
def dislike_user(user_id: int):
    result: Optional[User] = storage_session.unschedule_like(user_id=user_id)
    status = requests.status_codes.codes.ok if result is not None else requests.status_codes.codes.bad_request
    return make_response(jsonify({
        'message': 'User unscheduled' if result is not None else 'User not scheduled'
    }), status)


@app.route(app_routes['HIDE_USER'], methods=['POST'])
def hide_user(user_id: int):
    hidden_user: Optional[UserDao] = storage_session.hide_user(user_id=user_id)
    response_code: int = requests.status_codes.codes.ok
    if hidden_user is not None:
        app_request.pass_profile(user=hidden_user)
    else:
        response_code = requests.status_codes.codes.bad_request
    return make_response(jsonify({
        'message': 'User was hidden' if hidden_user is not None else 'User not found'
    }), response_code)


@app.route(app_routes['GET_LOGS'], methods=['GET'])
def get_logs():
    return make_response(jsonify({
        'logs': [log.to_dict() for log in Logs(storage=storage_session).get_logs_chunk()],
    }), requests.status_codes.codes.ok)


@app.route(app_routes['GET_ARCHIVE_LOGS'], methods=['GET'])
def get_archive_logs():
    logs: list[dict] = []
    try:
        from_log = request.args.get('from')
        if from_log is not None:
            logs = [log.to_dict() for log in Logs(storage=storage_session).get_archive_logs(from_log=int(from_log))]
    except ValueError:
        pass
    return make_response(jsonify({'logs': logs}), requests.status_codes.codes.ok)


@app.route(app_routes['GET_TAIL_LOGS'], methods=['GET'])
def get_tail_logs():
    logs: list[dict] = []
    try:
        to_log = request.args.get('to')
        if to_log is not None:
            logs = [log.to_dict() for log in Logs(storage=storage_session).get_latest_logs(to_log=int(to_log))]
    except ValueError:
        pass
    return make_response(jsonify({'logs': logs}), requests.status_codes.codes.ok)


@app.route(app_routes['SEARCH_LOGS'], methods=['GET'])
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


@app.route(app_routes['SAVE_API_TOKEN'], methods=['POST'])
def add_or_update_token(token: str):
    storage_session.add_update_api_key(key_value=token)
    return make_response(jsonify({
        'updated': True,
    }), requests.status_codes.codes.ok)


@app.route(app_routes['SAVE_BASE_URL'], methods=['POST'])
def add_or_update_base_url(url: str):
    storage_session.add_update_base_url(url_value=url)
    return make_response(jsonify({
        'updated': True,
    }), requests.status_codes.codes.ok)


@app.route(app_routes['SCHEDULE_LIKE'], methods=['POST'])
def schedule_like(user_id: int):
    storage_session.schedule_like(user_id=user_id)
    return make_response(jsonify({
        'scheduled': True,
    }), requests.status_codes.codes.ok)


@app.route(app_routes['GET_SETTINGS'], methods=['GET'])
def get_settings():
    return make_response(jsonify({
        'api_key': storage_session.get_api_key(),
        'base_url': storage_session.get_base_url(),
        'scheduled': storage_session.get_scheduled(),
        'teasers': storage_session.get_teasers(),
    }), requests.status_codes.codes.ok)


@app.route(app_routes['GET_SETTINGS_LIKES'], methods=['GET'])
def get_likes_remaining():
    url: str = 'https://%s/v2/profile?include=likes' % storage_session.get_base_url()
    response = app_request.make_api_call(url=url, method='GET')
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
