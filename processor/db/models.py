import datetime
from typing import List

from sqlalchemy import String, ForeignKey, TIMESTAMP, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=False),
    }


class User(Base):
    __tablename__ = 'user'

    city: Mapped[str] = mapped_column(String(100))
    created: Mapped[datetime.datetime]
    id: Mapped[int] = mapped_column(primary_key=True)
    liked: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String(100))
    s_number: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[str] = mapped_column(String(100))

    photos: Mapped[List['Photo']] = relationship(
        back_populates='user', cascade='all, delete-orphan',
    )

    def __repr__(self):
        return f'''
            User(city={self.city!r}, id={self.id!r}, name={self.name!r}, s_number={self.s_number!r},
            'user_id={self.user_id})
        '''


class Photo(Base):
    __tablename__ = 'photo'

    created: Mapped[datetime.datetime]
    id: Mapped[int] = mapped_column(primary_key=True)
    photo_id: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(back_populates='photos')

    def __repr__(self):
        return f'''
            Photo(created={self.created!r}, id={self.id!r}, photo_id={self.photo_id!r}, url={self.url!r}), \
            user_id={self.user_id!r}
        '''


class Settings(Base):
    __tablename__ = 'settings'
    daily_run_table_name = 'daily_like_last_run'
    teasers_setting = 'teasers_setting'

    created: Mapped[datetime.datetime]
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return f'Settings(created={self.created!r}, id={self.id!r}, name={self.name!r}, value={self.value!r})'


class Log(Base):
    __tablename__ = 'log'

    created: Mapped[datetime.datetime]
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()

    def __repr__(self):
        return f'Log(created={self.created!r}, id={self.id!r}, text={self.text!r})'
