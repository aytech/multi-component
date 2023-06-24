import datetime

from sqlalchemy.orm import Session

from enums.LogContext import LogContext
from enums.LogLevel import LogLevel
from models.Log import Log


class BaseService(object):
    session: Session

    def log_message(self, message: str, context: str, level: str = LogLevel.DEBUG):
        if level == LogLevel.DEBUG:
            print('[DEBUG]: %s' % message)
        else:
            with self.session as session:
                session.add(Log(
                    context=context,
                    created=datetime.datetime.now(),
                    level=level,
                    text=message,
                ))
                session.commit()

    def __init__(self, session: Session):
        self.session = session
