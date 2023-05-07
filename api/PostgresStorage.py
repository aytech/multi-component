import datetime
import json
import os
from typing import Optional

from sqlalchemy import create_engine, Select, select, func, update
from sqlalchemy.orm import Session

from db.dao import UserDao, PhotoDao
from db.models import User, Log, Settings, ScheduledLike
from utilities.LogContext import LogContext
from utilities.LogLevel import LogLevel


class PostgresStorage:
    session: Session
    logs_limit: int = 100

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
        statement: Select = select(User)
        if liked is not None:
            statement = statement.where(User.liked)
        # paginate
        statement = statement.where(User.visible).order_by(User.created.desc()).offset(
            (page - 1) * page_size).limit(page_size)
        self.log_message(message=str(statement), context=LogContext.SQL)
        return [self.get_user_dict(user) for user in self.session.scalars(statement=statement).all()]

    def list_users_by_id(self, ids: list[int]) -> list[dict]:
        statement: Select = select(User).where(User.visible).filter(User.id.in_(ids)).order_by(User.created.desc())
        return [self.get_user_dict(user) for user in self.session.scalars(statement=statement).all()]

    def search_users(self, name_partial: str, page: int = 1, size: int = 10):
        statement: Select = select(User).where(User.name.like('%{}%'.format(name_partial))).order_by(
            User.created.desc()).offset((page - 1) * size).limit(size)
        return [self.get_user_dict(user) for user in self.session.scalars(statement=statement).all()]

    def fetch_all_users_count(self, liked: bool or None = None) -> int:
        if liked:
            return self.session.query(func.count(User.id)).where(User.liked).scalar()
        return self.session.query(func.count(User.id)).scalar()

    def fetch_scheduled(self) -> list[int]:
        return [like.user_id for like in self.session.scalars(statement=select(ScheduledLike)).all()]

    def fetch_filtered_users_count(self, name_partial: str):
        return self.session.query(func.count(User.id)).where(User.name.like('%{}%'.format(name_partial))).scalar()

    def fetch_user_by_id(self, user_id: int) -> User:
        return self.session.scalars(statement=select(User).where(User.id == user_id)).one()

    def update_user(self, user: User):
        with self.session as session:
            session.execute(statement=update(User).where(User.id == user.id).values(liked=user.liked))
            session.commit()

    def log_message(self, message: str, context: LogContext, level: LogLevel = LogLevel.DEBUG):
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

    def get_logs(self, from_log: int = None, to_log: int = None) -> list[Log]:
        statement: Select = select(Log)
        # Fetching historical log
        if from_log is not None:
            statement = statement.where(Log.id < from_log)
        # Fetching live tail
        if from_log is None and to_log is not None:
            statement = statement.where(Log.id > to_log)
        # Standard ordering
        statement = statement.order_by(Log.created.desc()).limit(limit=self.logs_limit)
        return [log for log in self.session.scalars(statement=statement).all()]

    def search_logs(self, criteria: str) -> list[Log]:
        statement: Select = select(Log).where(Log.text.like('%{}%'.format(criteria))).order_by(Log.created.desc())
        return [log for log in self.session.scalars(statement=statement).all()]

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

    def hide_user(self, user_id: int) -> Optional[User]:
        with self.session as session:
            user: User = session.scalar(statement=select(User).where(User.id == user_id))
            if user is not None:
                user.visible = False
                session.commit()
                return user
        return None

    def schedule_like(self, user_id: int) -> Optional[User]:
        with self.session as session:
            user: User = session.scalar(statement=select(User).where(User.id == user_id))
            scheduled: ScheduledLike = session.scalar(
                statement=select(ScheduledLike).where(ScheduledLike.user_id == user_id))
            if user is not None and scheduled is None:
                session.add(ScheduledLike(
                    user_id=user_id
                ))
                session.commit()
                return user
        return None

    def unschedule_like(self, user_id: int) -> Optional[ScheduledLike]:
        with self.session as session:
            user: User = session.scalar(statement=select(User).where(User.id == user_id))
            scheduled: ScheduledLike = session.scalar(
                statement=select(ScheduledLike).where(ScheduledLike.user_id == user_id))
            if user is not None and scheduled is not None:
                session.delete(scheduled)
                session.commit()
                return scheduled
        return None

    def __init__(self):
        engine = create_engine('postgresql+psycopg://%s:%s@%s:%s/%s' % (
            os.environ.get('POSTGRES_USER'),
            os.environ.get('POSTGRES_PASSWORD'),
            os.environ.get('POSTGRES_HOST'),
            os.environ.get('POSTGRES_PORT'),
            os.environ.get('POSTGRES_DB'),
        ))
        self.session = Session(engine)
