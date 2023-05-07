import datetime
import re

from utilities.DateProcessor import DateProcessor


class PhotoDao:
    created: str
    photo_id: str
    url: str

    def __init__(self, photo_id: str, url: str):
        self.created = DateProcessor.get_current_date()
        self.photo_id = photo_id
        self.url = url

    def __str__(self):
        return f'''Photo(created={self.created}, url={self.url})'''


class UserDao:
    age: int
    bio: str
    birth_date: str
    city: str
    created: str
    distance: float
    liked: bool
    name: str
    photos: list[PhotoDao]
    s_number: int
    user_id: str

    def __init__(self, bio: str, distance_mi: int, liked: bool, name: str, s_number: int, user_id: str):
        self.age = 0
        self.bio = bio
        self.birth_date = ''
        self.city = ''
        self.created = DateProcessor.get_current_date()
        self.distance = 0 if distance_mi is None else (distance_mi * 1.6)
        self.liked = liked
        self.name = name
        self.photos = []
        self.s_number = s_number
        self.user_id = user_id

    def __str__(self):
        dao_str: str = f'''
            User(age={self.age}, bio={self.bio}, birth_date={self.birth_date}, city={self.city}, created={self.created}, 
            distance={self.distance}, liked={self.liked}, name={self.name}, 
            photos={[str(photo) for photo in self.photos]}, s_number={self.s_number}, user_id={self.user_id})
        '''
        dao_str = re.sub(r'\s+', ' ', dao_str)
        return dao_str.replace('\n', '').strip()


class ScheduledLikeDao:
    id: int
    user: UserDao

    def __init__(self, db_id: int, user: UserDao):
        self.id = db_id
        self.user = user


class UserTeaserDao:
    name: str

    def __init__(self, name: str):
        self.name = name


class RemainingLikesDao:
    likes_remaining: int
    rate_limited_until: datetime

    def __init__(self, likes_remaining: int, rate_limited_until: int = None):
        self.likes_remaining = likes_remaining
        if rate_limited_until is not None:
            # convert to seconds from millis
            seconds = rate_limited_until // 1000
            self.rate_limited_until = datetime.datetime.utcfromtimestamp(seconds)


class LikesResponseDao:
    likes_remaining: int
    match: bool
    status: int

    def __init__(self, likes_remaining: int = 0, match: bool = False, status: int = None):
        self.likes_remaining = likes_remaining
        self.match = match
        self.status = status
