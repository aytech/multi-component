import os

from sqlalchemy import create_engine, Select, select, func, update
from sqlalchemy.orm import Session

from dao import UserDao, PhotoDao
from models import User


class PostgresStorage:
    session: Session

    @staticmethod
    def get_user_dict(user: User) -> dict:
        user_dao: UserDao = UserDao(
            city=user.city,
            db_id=user.id,
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

    def fetch_all_users_count(self):
        return self.session.query(func.count(User.id)).scalar()

    def fetch_filtered_users_count(self, name_partial: str):
        return self.session.query(func.count(User.id)).where(User.name.like('%{}%'.format(name_partial))).scalar()

    def fetch_user_by_id(self, user_id: int) -> User:
        return self.session.scalars(statement=select(User).where(User.id == user_id)).one()

    def delete_user_by_id(self, user_id: int) -> None:
        with self.session as session:
            session.delete(self.fetch_user_by_id(user_id=user_id))
            session.commit()

    def update_user(self, user: User):
        with self.session as session:
            session.execute(statement=update(User).where(User.id == user.id).values(liked=user.liked))
            session.commit()

    def __init__(self):
        engine = create_engine('postgresql+psycopg://%s:%s@%s:%s/%s' % (
            os.environ.get('POSTGRES_USER'),
            os.environ.get('POSTGRES_PASSWORD'),
            os.environ.get('POSTGRES_HOST'),
            os.environ.get('POSTGRES_PORT'),
            os.environ.get('POSTGRES_DB'),
        ))
        self.session = Session(engine)
