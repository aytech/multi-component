import datetime
import json
import os
from typing import Optional

from sqlalchemy import create_engine, Select, select, func, update
from sqlalchemy.orm import Session

from db.dao import UserDao, PhotoDao
from db.models import User, Log, Settings


class PostgresStorage:
    session: Session

    @staticmethod
    def get_user_dict(user: User) -> dict:
        user_dao: UserDao = UserDao(
            bio=user.bio,
            birth_date=user.birth_date,
            city=user.city,
            created=user.get_created(),
            db_id=user.id,
            distance_mi=user.distance_mi,
            liked=user.liked,
            name=user.name,
            s_number=user.s_number,
            user_id=user.user_id
        )
        user_dao.age = user.get_age()
        user_dao.photos = [PhotoDao(
            photo_id=photo.photo_id,
            url=photo.url
        ).__dict__ for photo in user.photos]
        return user_dao.__dict__

    def list_users(self, page: int, page_size: int = 10, liked: bool or None = None) -> list[dict]:
        users: list[dict] = []
        statement: Select = select(User)
        if liked is not None:
            statement = statement.where(User.liked == liked)
        # paginate
        statement = statement.order_by(User.created.desc()).offset((page - 1) * page_size).limit(page_size)
        for user in self.session.scalars(statement=statement).all():
            users.append(self.get_user_dict(user=user))
        return users

    def search_users(self, name_partial: str, page: int = 1, size: int = 10, liked: bool or None = None):
        users: list[dict] = []
        statement: Select = select(User).where(User.name.like('%{}%'.format(name_partial)))
        if liked is not None:
            statement = statement.where(User.liked == liked)
        # paginate
        statement = statement.order_by(User.created.desc()).offset((page - 1) * size).limit(size)
        for user in self.session.scalars(statement=statement).all():
            users.append(self.get_user_dict(user=user))
        return users

    def fetch_all_users_count(self):
        return self.session.query(func.count(User.id)).scalar()

    def fetch_filtered_users_count(self, name_partial: str):
        return self.session.query(func.count(User.id)).where(User.name.like('%{}%'.format(name_partial))).scalar()

    def fetch_user_by_id(self, user_id: int) -> User:
        return self.session.scalars(statement=select(User).where(User.id == user_id)).one()

    def delete_user_by_id(self, user_id: int) -> User:
        user: User = self.fetch_user_by_id(user_id=user_id)
        with self.session as session:
            session.delete(self.fetch_user_by_id(user_id=user_id))
            session.commit()
        return user

    def update_user(self, user: User):
        with self.session as session:
            session.execute(statement=update(User).where(User.id == user.id).values(liked=user.liked))
            session.commit()

    def get_logs(self, limit: int, from_index: int = None):
        statement: Select = select(Log)
        if from_index is not None:
            statement = statement.where(Log.id <= from_index)
        statement = statement.order_by(Log.id.desc()).limit(limit=limit)
        return self.session.scalars(statement=statement).all()

    def is_last_log(self, log_id: int) -> bool:
        return self.session.query(Log.id).order_by(Log.id.desc()).limit(1).scalar() <= log_id

    def add_update_api_key(self, key_value: str):
        statement: Select = select(Settings).where(Settings.name == Settings.api_key_setting)
        token_setting: Settings = self.session.scalar(statement=statement)
        if token_setting is None:
            token_setting = Settings(
                created=datetime.datetime.now(),
                name=Settings.api_key_setting,
            )
        token_setting.value = key_value
        with self.session as session:
            session.add(token_setting)
            session.commit()

    def add_update_base_url(self, url_value: str):
        statement: Select = select(Settings).where(Settings.name == Settings.base_url_setting)
        url_setting: Settings = self.session.scalar(statement=statement)
        if url_setting is None:
            url_setting = Settings(
                created=datetime.datetime.now(),
                name=Settings.base_url_setting,
            )
        url_setting.value = url_value
        with self.session as session:
            session.add(url_setting)
            session.commit()

    def get_teasers(self):
        statement: Select = select(Settings).where(Settings.name == Settings.teasers_setting)
        settings: Settings = self.session.scalar(statement=statement)
        if settings is None:
            return []
        return json.loads(settings.value)

    def get_api_key(self):
        statement: Select = select(Settings).where(Settings.name == Settings.api_key_setting)
        settings: Settings = self.session.scalar(statement=statement)
        return None if settings is None else settings.value

    def get_base_url(self) -> Optional[Settings]:
        statement: Select = select(Settings).where(Settings.name == Settings.base_url_setting)
        settings: Settings = self.session.scalar(statement=statement)
        return None if settings is None else settings.value

    def __init__(self):
        engine = create_engine('postgresql+psycopg://%s:%s@%s:%s/%s' % (
            os.environ.get('POSTGRES_USER'),
            os.environ.get('POSTGRES_PASSWORD'),
            os.environ.get('POSTGRES_HOST'),
            os.environ.get('POSTGRES_PORT'),
            os.environ.get('POSTGRES_DB'),
        ))
        self.session = Session(engine)
