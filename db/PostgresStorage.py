import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import User, Log


class PostgresStorage:
    session: Session

    def get_user(self, user_id: str) -> User:
        statement = select(User).where(User.user_id == user_id)
        return self.session.scalars(statement=statement).one_or_none()

    def add_user(self, user: User):
        with self.session as session:
            session.add(user)
            session.commit()

    def add_message(self, message: str):
        with self.session as session:
            message = Log(
                created=datetime.datetime.now(),
                text=message
            )
            session.add(message)
            session.commit()

    def __init__(self):
        engine = create_engine('postgresql+psycopg://oleg:postgres@storage/tinder')
        self.session = Session(engine)
