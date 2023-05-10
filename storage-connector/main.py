import logging
from concurrent import futures
import os

import grpc
import protos.connector_pb2
import protos.connector_pb2_grpc
from services.Profiler import Profiler

grpc_port: str = os.environ.get('GRPC_PORT', default='50051')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protos.connector_pb2_grpc.add_ConnectorServicer_to_server(Profiler(), server=server)
    server.add_insecure_port('[::]:' + grpc_port)
    server.start()
    print("Server started, listening on " + grpc_port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
