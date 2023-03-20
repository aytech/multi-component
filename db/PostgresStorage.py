import datetime
from typing import Optional

from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.dao import UserDao, PhotoDao
from db.models import User, Log, Photo


class PostgresStorage:
    session: Session

    def get_user(self, user_id: str) -> Optional[UserDao]:
        statement = select(User).where(User.user_id == user_id)
        try:
            user: User = self.session.scalars(statement=statement).one()
            user_dao: UserDao = UserDao(
                city=user.city,
                name=user.name,
                s_number=user.s_number,
                user_id=user.user_id
            )
            user_dao.photos = [PhotoDao(
                photo_id=photo.photo_id,
                url=photo.url
            ) for photo in user.photos]
            return user_dao
        except NoResultFound:
            return None

    def add_user(self, user: UserDao):
        creation_date = datetime.datetime.now()
        with self.session as session:
            session.add(User(
                city=user.city,
                created=creation_date,
                name=user.name,
                photos=[Photo(
                    created=creation_date,
                    photo_id=photo.photo_id,
                    url=photo.url
                ) for photo in user.photos],
                s_number=user.s_number,
                user_id=user.user_id
            ))
            session.commit()

    def add_message(self, message: str):
        with self.session as session:
            session.add(Log(
                created=datetime.datetime.now(),
                text=message
            ))
            session.commit()

    def __init__(self):
        engine = create_engine('postgresql+psycopg://oleg:postgres@storage/tinder')
        self.session = Session(engine)
