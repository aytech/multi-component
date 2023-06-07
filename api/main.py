import os
from typing import Optional

import grpc
import requests as requests
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_restful import Api
from google.protobuf.json_format import MessageToJson

import proto.actions_pb2_grpc
import proto.logs_pb2_grpc
import proto.profiles_pb2_grpc
import proto.settings_pb2_grpc
from utilities.RemainingLikesDao import RemainingLikesDao
from proto.actions_pb2 import ActionsRequest, ActionsReply
from proto.logs_pb2 import LogsRequest, LogsReply
from proto.profiles_pb2 import ProfilesRequest, ProfilesSearchRequest
from proto.settings_pb2 import SettingsRequest, Empty, FetchSettingsValueReply
from routes import app_routes
from utilities.Request import Request
from utilities.Results import Results

grpc_host: str = os.environ.get('GRPC_HOST', default='localhost')
grpc_port: str = os.environ.get('GRPC_PORT', default='50051')

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
        stub = proto.profiles_pb2_grpc.ProfilesStub(channel=channel)
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
        stub = proto.profiles_pb2_grpc.ProfilesStub(channel=channel)
        response = stub.SearchProfiles(ProfilesSearchRequest(value=name, status=status, page=page, page_size=size))
        return make_response(MessageToJson(response.reply), requests.status_codes.codes.ok)


@app.route(app_routes['SCHEDULE_LIKE'], methods=['POST'])
def like_user(user_id: int):
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = proto.actions_pb2_grpc.ActionsStub(channel=channel)
        response = stub.ScheduleLike(ActionsRequest(user_id=user_id))
        return make_response(MessageToJson(response), requests.status_codes.codes.ok)


@app.route(app_routes['UNSCHEDULE_LIKE'], methods=['POST'])
def dislike_user(user_id: int):
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = proto.actions_pb2_grpc.ActionsStub(channel=channel)
        response = stub.UnScheduleLike(ActionsRequest(user_id=user_id))
        return make_response(MessageToJson(response), requests.status_codes.codes.ok)


@app.route(app_routes['HIDE_USER'], methods=['POST'])
def hide_user(user_id: int):
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub_actions = proto.actions_pb2_grpc.ActionsStub(channel=channel)
        stub_settings = proto.settings_pb2_grpc.SettingsStub(channel=channel)
        response: ActionsReply = stub_actions.HideProfile(ActionsRequest(user_id=user_id))
        if response.success:
            api_key: FetchSettingsValueReply = stub_settings.FetchApiKey(Empty())
            base_url: FetchSettingsValueReply = stub_settings.FetchBaseUrl(Empty())
            app_request: Request = Request(api_key=api_key.value, base_url=base_url.value)
            app_request.pass_profile(user_id=user_id, s_number=response.s_number)
            return make_response(MessageToJson(response), requests.status_codes.codes.ok)
        return make_response(MessageToJson(response), requests.status_codes.codes.bad_request)


@app.route(app_routes['GET_LOGS'], methods=['GET'])
def get_logs():
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = proto.logs_pb2_grpc.LogsStub(channel=channel)
        response: LogsReply = stub.FetchLogs(LogsRequest())
        return make_response(MessageToJson(response), requests.status_codes.codes.ok)


@app.route(app_routes['GET_ARCHIVE_LOGS'], methods=['GET'])
def get_archive_logs():
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = proto.logs_pb2_grpc.LogsStub(channel=channel)
        from_log = request.args.get('from')
        if from_log is not None:
            response: LogsReply = stub.FetchLogs(LogsRequest(from_log=int(from_log)))
            if len(response.logs) > 0:
                return make_response(MessageToJson(response), requests.status_codes.codes.ok)
        return make_response(jsonify({'logs': []}), requests.status_codes.codes.ok)


@app.route(app_routes['GET_TAIL_LOGS'], methods=['GET'])
def get_tail_logs():
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = proto.logs_pb2_grpc.LogsStub(channel=channel)
        to_log = request.args.get('to')
        if to_log is not None:
            response: LogsReply = stub.FetchLogs(LogsRequest(to_log=int(to_log)))
            if len(response.logs) > 0:
                return make_response(MessageToJson(response), requests.status_codes.codes.ok)
        return make_response(jsonify({'logs': []}), requests.status_codes.codes.ok)


@app.route(app_routes['SEARCH_LOGS'], methods=['GET'])
def search_logs():
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = proto.logs_pb2_grpc.LogsStub(channel=channel)
        criteria = request.args.get('search')
        if criteria is not None:
            response: LogsReply = stub.SearchLogs(LogsRequest(search_text=criteria))
            if len(response.logs) > 0:
                return make_response(MessageToJson(response), requests.status_codes.codes.ok)
        return make_response(jsonify({'logs': []}), requests.status_codes.codes.ok)


@app.route(app_routes['SAVE_API_TOKEN'], methods=['POST'])
def add_or_update_token(token: str):
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = proto.settings_pb2_grpc.SettingsStub(channel=channel)
        return stub.AddUpdateApiKey(SettingsRequest(value=token))


@app.route(app_routes['SAVE_BASE_URL'], methods=['POST'])
def add_or_update_base_url(url: str):
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = proto.settings_pb2_grpc.SettingsStub(channel=channel)
        return stub.AddUpdateBaseUrl(SettingsRequest(value=url))


@app.route(app_routes['GET_SETTINGS'], methods=['GET'])
def get_settings():
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = proto.settings_pb2_grpc.SettingsStub(channel=channel)
        return make_response(MessageToJson(stub.FetchSettings(Empty())), requests.status_codes.codes.ok)


@app.route(app_routes['GET_SETTINGS_LIKES'], methods=['GET'])
def get_likes_remaining():
    with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
        stub = proto.settings_pb2_grpc.SettingsStub(channel=channel)
        api_key: FetchSettingsValueReply = stub.FetchApiKey(Empty())
        base_url: FetchSettingsValueReply = stub.FetchBaseUrl(Empty())
        app_request: Request = Request(api_key=api_key.value, base_url=base_url.value)
        url: str = 'https://%s/v2/profile?include=likes' % base_url.value
        response = app_request.make_api_call(url=url, method='GET')
        likes: RemainingLikesDao = Results.remaining_likes(response_data=response.data.decode('utf-8'))
        return make_response(jsonify(likes.to_dict()), requests.status_codes.codes.ok)


if __name__ == '__main__':
    app.run(debug=True)
