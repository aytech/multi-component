import grpc
from sqlalchemy import Select, select

from enums.LogContext import LogContext
from models.Log import Log
from protos.logs_pb2 import LogsRequest, LogsReply
from protos.logs_pb2_grpc import LogsServicer
from services.BaseService import BaseService


class Logs(LogsServicer, BaseService):
    log_limit: int = 100

    @staticmethod
    def get_log(log: Log) -> LogsReply.Log:
        log = LogsReply.Log(
            context=log.context,
            created=log.created.strftime('%d %b %Y %H:%M:%S'),
            id=log.id,
            level=log.level,
            text=log.text
        )
        return log

    def FetchLogs(self, request: LogsRequest, context: grpc.ServicerContext) -> LogsReply:
        statement: Select = select(Log)
        # Fetching historical log
        if request.from_log > 0:
            statement = statement.filter(Log.id < request.from_log)
        # Fetching live tail
        if request.to_log > 0:
            statement = statement.filter(Log.id > request.to_log)
        # Standard ordering
        statement = statement.order_by(Log.created.desc()).limit(limit=self.log_limit)
        self.log_message(message=str(statement), context=LogContext.SQL)
        logs = self.session.scalars(statement=statement).all()
        return LogsReply(logs=[self.get_log(log=log) for log in self.session.scalars(statement=statement).all()])

    def SearchLogs(self, request: LogsRequest, context: grpc.ServicerContext) -> LogsReply:
        statement: Select = select(Log).where(Log.text.like('%{}%'.format(request.search_text))).order_by(
            Log.created.desc())
        return LogsReply(logs=[self.get_log(log=log) for log in self.session.scalars(statement=statement).all()])
