from typing import Optional

from models.Photo import Photo


class User:
    city: Optional[str] = None
    id: str
    name: str
    photos: list[Photo] = []
    s_number: int

    def __init__(self, user_id, name, s_number):
        self.id = user_id
        self.name = name
        self.s_number = s_number
