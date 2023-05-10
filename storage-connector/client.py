import logging
import grpc

import protos.connector_pb2
import protos.connector_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print('Trying to fetch profiles ...')
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = protos.connector_pb2_grpc.ConnectorStub(channel=channel)
        # response = stub.FetchProfiles(protos.connector_pb2.ProfilesRequest(status='new', page=1, page_size=10))
        response = stub.SearchProfiles(
            protos.connector_pb2.ProfilesSearchRequest(value='Ren', status='new', page=1, page_size=10))
    for profile in response.reply.profiles:
        print('Profile received: ' + profile.name)
    print('Total: ', response.reply.total)


if __name__ == '__main__':
    logging.basicConfig()
    run()
