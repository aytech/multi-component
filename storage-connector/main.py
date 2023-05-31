import logging
from concurrent import futures
import os

import grpc
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import protos.actions_pb2_grpc
import protos.logs_pb2_grpc
import protos.profiles_pb2_grpc
from services.Actions import Actions
from services.Logs import Logs
from services.Profiles import Profiles

grpc_port: str = os.environ.get('GRPC_PORT', default='50051')
pg_db: str = os.environ.get('POSTGRES_DB')
pg_host: str = os.environ.get('POSTGRES_HOST')
pg_password: str = os.environ.get('POSTGRES_PASSWORD')
pg_port: str = os.environ.get('POSTGRES_PORT')
pg_user: str = os.environ.get('POSTGRES_USER')


def serve():
    engine = create_engine('postgresql+psycopg://%s:%s@%s:%s/%s' % (pg_user, pg_password, pg_host, pg_port, pg_db))
    session: Session = Session(engine)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add services
    protos.profiles_pb2_grpc.add_ProfilesServicer_to_server(Profiles(session=session), server=server)
    protos.actions_pb2_grpc.add_ActionsServicer_to_server(Actions(session=session), server=server)
    protos.logs_pb2_grpc.add_LogsServicer_to_server(Logs(session=session), server=server)

    server.add_insecure_port('[::]:' + grpc_port)
    server.start()
    print("Server started, listening on " + grpc_port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
