import datetime
from typing import List

from sqlalchemy import Text, String, Integer, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.Base import Base


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


class User(Base):
    __tablename__ = 'user'

    bio: Mapped[str] = mapped_column(Text)
    birth_date: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    created: Mapped[datetime.datetime]
    distance_mi: Mapped[int] = mapped_column(Integer)
    id: Mapped[int] = mapped_column(primary_key=True)
    liked: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String(100))
    s_number: Mapped[int] = mapped_column(BigInteger)
    scheduled: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[str] = mapped_column(String(100))
    visible: Mapped[bool] = mapped_column(Boolean, default=True)

    photos: Mapped[List['Photo']] = relationship(
        back_populates='user', cascade='all, delete-orphan',
    )

    def __repr__(self):
        return f'''
            User(city={self.city!r}, id={self.id!r}, name={self.name!r}, s_number={self.s_number!r},
            'user_id={self.user_id})
        '''

    def get_age(self):
        if self.birth_date is None:
            return 0
        try:
            birth_date: datetime = datetime.datetime.strptime(str(self.birth_date), '%d %b, %Y')
            return int((datetime.datetime.now() - birth_date).days / 365)
        except ValueError:
            return 0

    def get_created(self):
        created: datetime = self.created.strftime('%d %b %H:%M:%S')
        return created
