import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from models.Base import Base


class Log(Base, SerializerMixin):
    __tablename__ = 'log'

    context: Mapped[str] = mapped_column(String(20))
    created: Mapped[datetime.datetime]
    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[str] = mapped_column(String(10))
    text: Mapped[str] = mapped_column()

    def __repr__(self):
        return f'Log(created={self.created!r}, id={self.id!r}, text={self.text!r})'
