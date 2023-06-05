# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import logs_pb2 as protos_dot_logs__pb2


class LogsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FetchLogs = channel.unary_unary(
                '/Logs/FetchLogs',
                request_serializer=protos_dot_logs__pb2.LogsRequest.SerializeToString,
                response_deserializer=protos_dot_logs__pb2.LogsReply.FromString,
                )
        self.SearchLogs = channel.unary_unary(
                '/Logs/SearchLogs',
                request_serializer=protos_dot_logs__pb2.LogsRequest.SerializeToString,
                response_deserializer=protos_dot_logs__pb2.LogsReply.FromString,
                )


class LogsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def FetchLogs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchLogs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LogsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FetchLogs': grpc.unary_unary_rpc_method_handler(
                    servicer.FetchLogs,
                    request_deserializer=protos_dot_logs__pb2.LogsRequest.FromString,
                    response_serializer=protos_dot_logs__pb2.LogsReply.SerializeToString,
            ),
            'SearchLogs': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchLogs,
                    request_deserializer=protos_dot_logs__pb2.LogsRequest.FromString,
                    response_serializer=protos_dot_logs__pb2.LogsReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Logs', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Logs(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def FetchLogs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Logs/FetchLogs',
            protos_dot_logs__pb2.LogsRequest.SerializeToString,
            protos_dot_logs__pb2.LogsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SearchLogs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Logs/SearchLogs',
            protos_dot_logs__pb2.LogsRequest.SerializeToString,
            protos_dot_logs__pb2.LogsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
