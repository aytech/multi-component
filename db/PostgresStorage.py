import datetime
from typing import Optional

from sqlalchemy import create_engine, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.dao import UserDao, PhotoDao
from db.models import User, Log, Photo, Settings


class PostgresStorage:
    session: Session

    @staticmethod
    def get_user_dao(user: User) -> UserDao:
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

    def get_user(self, user_id: str) -> Optional[UserDao]:
        statement = select(User).where(User.user_id == user_id)
        try:
            return self.get_user_dao(self.session.scalars(statement=statement).one())
        except NoResultFound:
            return None

    def get_users_by_name(self, name: str) -> list[UserDao]:
        statement = select(User).where(User.name == name)
        users: list[UserDao] = []
        try:
            for user in self.session.scalars(statement=statement).all():
                users.append(self.get_user_dao(user))
        except NoResultFound:
            pass
        return users

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

    def add_message(self, message: str, persist: bool = False):
        print('[DEBUG]: %s' % message)
        if persist:
            with self.session as session:
                session.add(Log(
                    created=datetime.datetime.now(),
                    text=message
                ))
                session.commit()

    def record_daily_like_run(self):
        time_stamp = datetime.datetime.now()
        setting_model = self.get_daily_run_setting()

        with self.session as session:
            if setting_model is None:
                session.add(Settings(
                    created=time_stamp,
                    name=Settings.daily_run_table_name,
                    value=str(time_stamp)
                ))
                session.commit()
            else:
                session.execute(
                    statement=update(Settings).where(Settings.id == setting_model.id).values(value=str(time_stamp)))
            session.commit()

    def get_daily_run_setting(self) -> Optional[Settings]:
        setting_name: str = Settings.daily_run_table_name
        select_statement = select(Settings).where(Settings.name == setting_name)
        return self.session.scalars(statement=select_statement).one_or_none()

    def __init__(self):
        engine = create_engine('postgresql+psycopg://oleg:postgres@storage/tinder')
        self.session = Session(engine)
