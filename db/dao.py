from typing import Optional


class PhotoDao:
    created: str
    photo_id: str
    url: str

    def __init__(self, photo_id: str, url: str):
        self.photo_id = photo_id
        self.url = url


class UserDao:
    city: Optional[str]
    created: str
    name: str
    photos: list[PhotoDao]
    s_number: int
    user_id: str

    def __init__(self, name: str, s_number: int, user_id: str, city: Optional[str] = None):
        self.city = city
        self.name = name
        self.s_number = s_number
        self.user_id = user_id
