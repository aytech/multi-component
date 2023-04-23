import datetime
import json
import os
from typing import Optional

from sqlalchemy import create_engine, select, update, Select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.dao import UserDao, PhotoDao
from db.models import User, Log, Photo, Settings
from utilities.DateProcessor import DateProcessor


class PostgresStorage:
    session: Session

    @staticmethod
    def get_user_dao(user: User) -> UserDao:
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
        ) for photo in user.photos]
        return user_dao

    def get_user(self, user_id: str) -> Optional[UserDao]:
        statement = select(User).where(User.user_id == user_id)
        try:
            return self.get_user_dao(self.session.scalars(statement=statement).one())
        except NoResultFound:
            return None

    def get_users_by_name(self, name: str) -> list[UserDao]:
        users: list[UserDao] = []
        statement: Select = select(User).where(User.name == name)
        for user in self.session.scalars(statement=statement).all():
            users.append(self.get_user_dao(user=user))
        return users

    def get_user_by_user_id(self, user_id: str) -> Optional[UserDao]:
        statement = select(User).where(User.user_id == user_id)
        try:
            return self.get_user_dao(self.session.scalars(statement=statement).one())
        except NoResultFound:
            return None

    def add_user(self, user: UserDao):
        creation_date = datetime.datetime.now()
        with self.session as session:
            session.add(User(
                city=user.city,
                created=creation_date,
                liked=user.liked,
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

    def add_message(self, message: str, persist: bool = True):
        print('[DEBUG][%s]: %s' % (DateProcessor.get_current_date(), message,))
        if persist:
            with self.session as session:
                session.add(Log(
                    created=datetime.datetime.now(),
                    text=message
                ))
                session.commit()

    def update_user_like_status(self, user_id: str, status: bool):
        with self.session as session:
            session.execute(statement=update(User).where(User.user_id == user_id).values(liked=status))
            session.commit()

    def get_api_key(self) -> Optional[str]:
        statement: Select = select(Settings).where(Settings.name == Settings.api_key_setting)
        api_key: Settings = self.session.scalar(statement=statement)
        return None if api_key is None else api_key.value

    def get_base_url(self) -> Optional[str]:
        statement: Select = select(Settings).where(Settings.name == Settings.base_url_setting)
        base_url: Settings = self.session.scalar(statement=statement)
        return None if base_url is None else base_url.value

    def renew_user(self, user_dao: UserDao):
        user: User = self.session.scalars(statement=select(User).where(User.user_id == user_dao.user_id)).one()
        with self.session as session:
            session.delete(user)
            session.commit()
        self.add_user(user=user_dao)

    def add_teaser(self, teaser: str):
        statement: Select = select(Settings).where(Settings.name == Settings.teasers_setting)
        teaser_setting: Settings = self.session.scalar(statement=statement)
        teasers: list[str] = []
        if teaser_setting is None:
            teaser_setting = Settings(
                created=datetime.datetime.now(),
                name=Settings.teasers_setting,
            )
        else:
            teasers = json.loads(teaser_setting.value)
        if teaser not in teasers:
            teasers.append(teaser)
            teaser_setting.value = json.dumps(teasers)
            with self.session as session:
                session.add(teaser_setting)
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
