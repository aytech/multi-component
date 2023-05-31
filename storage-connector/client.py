import logging
import grpc

import protos.actions_pb2
import protos.actions_pb2_grpc
import protos.logs_pb2
import protos.logs_pb2_grpc
import protos.profiles_pb2
import protos.profiles_pb2_grpc

from protos.actions_pb2 import ActionsRequest, ActionsReply
from protos.logs_pb2 import LogsRequest, LogsReply
from protos.profiles_pb2 import ProfilesRequest, ProfilesSearchRequest


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print('Trying to fetch profiles ...')
    with grpc.insecure_channel('localhost:50051') as channel:
        # Profiles
        # profile_stub = protos.profiles_pb2_grpc.ProfilesStub(channel=channel)
        # response = profile_stub.FetchProfiles(ProfilesRequest(status='new', page=1, page_size=10))
        # response = profile_stub.SearchProfiles(ProfilesSearchRequest(value='Ren', status='new', page=1, page_size=10))
        # for profile in response.reply.profiles:
        #     print('Profile received: %s' % profile.id)
        # print('Total: ', response.reply.total)
        # Actions
        # actions_stub = protos.actions_pb2_grpc.ActionsStub(channel=channel)
        # like_response: LikeReply = actions_stub.ScheduleLike(LikeRequest(user_id=33081))
        # print('Like response: status: %s, message: %s' % (like_response.success, like_response.message))
        # dislike_response: LikeReply = actions_stub.UnScheduleLike(LikeRequest(user_id=33081))
        # print('Dislike response: status: %s, message: %s' % (dislike_response.success, dislike_response.message))
        # dupl_response: LikeReply = actions_stub.UnScheduleLike(LikeRequest(user_id=33081))
        # print('Duplicate response: status: %s, message: %s' % (dupl_response.success, dupl_response.message))
        # Logs
        logs_stub = protos.logs_pb2_grpc.LogsStub(channel=channel)
        logs_response: LogsReply = logs_stub.FetchLogs(LogsRequest())
        for log in logs_response.logs:
            print('Log: %s' % log.created)


if __name__ == '__main__':
    logging.basicConfig()
    run()
