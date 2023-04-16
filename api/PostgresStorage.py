import os

from sqlalchemy import create_engine, Select, select
from sqlalchemy.orm import Session

from dao import UserDao, PhotoDao
from models import User


class PostgresStorage:
    session: Session

    @staticmethod
    def get_user_dict(user: User) -> dict:
        user_dao: UserDao = UserDao(
            city=user.city,
            liked=user.liked,
            name=user.name,
            s_number=user.s_number,
            user_id=user.user_id
        )
        user_dao.photos = [PhotoDao(
            photo_id=photo.photo_id,
            url=photo.url
        ).__dict__ for photo in user.photos]
        return user_dao.__dict__

    def list_users(self, page: int, page_size: int = 10) -> list[dict]:
        users: list[dict] = []
        statement: Select = select(User).order_by(User.created.desc()).offset((page - 1) * page_size).limit(page_size)
        for user in self.session.scalars(statement=statement).all():
            users.append(self.get_user_dict(user=user))
        return users

    def search_users(self, name_partial: str, page: int = 1, page_size: int = 10) -> list[dict]:
        users: list[dict] = []
        statement: Select = select(User).where(User.name.like('%{}%'.format(name_partial))) \
            .order_by(User.created.desc()).offset((page - 1) * page_size).limit(page_size)
        for user in self.session.scalars(statement=statement).all():
            users.append(self.get_user_dict(user=user))
        return users

    def __init__(self):
        engine = create_engine('postgresql+psycopg://%s:%s@%s:%s/%s' % (
            os.environ.get('POSTGRES_USER'),
            os.environ.get('POSTGRES_PASSWORD'),
            os.environ.get('POSTGRES_HOST'),
            os.environ.get('POSTGRES_PORT'),
            os.environ.get('POSTGRES_DB'),
        ))
        self.session = Session(engine)
