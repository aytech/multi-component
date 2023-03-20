from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
from models import User


class Photo(Base):
    __tablename__ = 'photo'

    id: Mapped[int] = mapped_column(primary_key=True)
    photo_id: Mapped[str] = mapped_column(String(20))
    url: Mapped[str] = mapped_column()

    user: Mapped[User] = relationship(back_populates='user')

    def __repr__(self):
        return f'Photo(id={self.id!r}, photo_id={self.photo_id!r}, url={self.url!r})'
