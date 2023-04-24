from datetime import datetime
from typing import Optional


class PhotoDao:
    created: str
    photo_id: str
    url: str

    def __init__(self, photo_id: str, url: str):
        self.photo_id = photo_id
        self.url = url

    def __str__(self):
        return f'''Photo(url={self.url!r})'''


class UserDao:
    city: Optional[str]
    created: str
    id: int
    liked: bool
    name: str
    photos: list[PhotoDao]
    s_number: int
    user_id: str

    def __init__(self, db_id: int, liked: bool, name: str, s_number: int, user_id: str, city: Optional[str] = None):
        self.city = city
        self.id = db_id
        self.liked = liked
        self.name = name
        self.s_number = s_number
        self.user_id = user_id

    def __str__(self):
        return f'''
            User(city={self.city!r}, id={self.id}, liked={self.liked!r},, name={self.name!r},
            photos={[str(photo) for photo in self.photos]} s_number={self.s_number!r}, 'user_id={self.user_id})
        '''


class RemainingLikesDao:
    likes_remaining: int
    rate_limited_until: datetime

    def __init__(self, likes_remaining: int, rate_limited_until: int = None):
        self.likes_remaining = likes_remaining
        if rate_limited_until is None:
            self.rate_limited_until = datetime.now()
        else:
            # convert to seconds from millis
            seconds = rate_limited_until // 1000
            self.rate_limited_until = datetime.utcfromtimestamp(seconds)

    def to_dict(self):
        return {'likes_remaining': self.likes_remaining, 'rate_limited_until': self.rate_limited_until}
