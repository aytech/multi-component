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
    created: str
    distance: float
    id: int
    liked: bool
    name: str
    photos: list[PhotoDao]
    s_number: int
    user_id: str

    def __init__(self, liked: bool, name: str, s_number: int, user_id: str, db_id: int = 0,
                 photos: list[PhotoDao] = None):
        self.age = 0
        self.bio = ''
        self.birth_date = ''
        self.city = ''
        self.created = DateProcessor.get_current_date()
        self.id = db_id
        self.liked = liked
        self.name = name
        self.photos = [] if photos is None else photos
        self.s_number = s_number
        self.user_id = user_id

    def set_distance(self, distance_mi: int):
        self.distance = 0 if distance_mi is None else (distance_mi * 1.6)

    def __str__(self):
        dao_str: str = f'''
            User(age={self.age}, bio={self.bio}, birth_date={self.birth_date}, city={self.city}, created={self.created},
            distance={self.distance}, liked={self.liked}, name={self.name},
            photos={[str(photo) for photo in self.photos]}, s_number={self.s_number}, user_id={self.user_id})
        '''
        dao_str = re.sub(r'\s+', ' ', dao_str)
        return dao_str.replace('\n', '').strip()


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
    likes_remaining: int = None
    match: bool
    status: int

    def __init__(self, match: bool = False, status: int = None):
        self.match = match
        self.status = status
