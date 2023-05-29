# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import actions_pb2 as protos_dot_actions__pb2


class ActionsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ScheduleLike = channel.unary_unary(
                '/Actions/ScheduleLike',
                request_serializer=protos_dot_actions__pb2.LikeRequest.SerializeToString,
                response_deserializer=protos_dot_actions__pb2.LikeReply.FromString,
                )
        self.UnScheduleLike = channel.unary_unary(
                '/Actions/UnScheduleLike',
                request_serializer=protos_dot_actions__pb2.LikeRequest.SerializeToString,
                response_deserializer=protos_dot_actions__pb2.LikeReply.FromString,
                )


class ActionsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ScheduleLike(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnScheduleLike(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ActionsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ScheduleLike': grpc.unary_unary_rpc_method_handler(
                    servicer.ScheduleLike,
                    request_deserializer=protos_dot_actions__pb2.LikeRequest.FromString,
                    response_serializer=protos_dot_actions__pb2.LikeReply.SerializeToString,
            ),
            'UnScheduleLike': grpc.unary_unary_rpc_method_handler(
                    servicer.UnScheduleLike,
                    request_deserializer=protos_dot_actions__pb2.LikeRequest.FromString,
                    response_serializer=protos_dot_actions__pb2.LikeReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Actions', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Actions(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ScheduleLike(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Actions/ScheduleLike',
            protos_dot_actions__pb2.LikeRequest.SerializeToString,
            protos_dot_actions__pb2.LikeReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UnScheduleLike(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Actions/UnScheduleLike',
            protos_dot_actions__pb2.LikeRequest.SerializeToString,
            protos_dot_actions__pb2.LikeReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
