import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from models.Base import Base


class Settings(Base, SerializerMixin):
    __tablename__ = 'settings'

    api_key_setting = 'api_key'
    base_url_setting = 'base_url'
    teasers_setting = 'teasers'

    created: Mapped[datetime.datetime]
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return f'Settings(created={self.created!r}, id={self.id!r}, name={self.name!r}, value={self.value!r})'
