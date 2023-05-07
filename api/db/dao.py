import datetime
import decimal


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
    age: int
    bio: str
    birth_date: str
    city: str
    created: str
    distance: decimal
    id: int
    liked: bool
    name: str
    photos: list[PhotoDao]
    s_number: int
    user_id: str

    def __init__(self, bio: str, birth_date: str, city: str, created: str, distance_mi: float, db_id: int, liked: bool,
                 name: str, s_number: int, user_id: str):
        self.age = 0
        self.bio = bio
        self.birth_date = birth_date
        self.city = city
        self.created = created
        self.distance = 0 if distance_mi is None else round(distance_mi * 1.6, 2)
        self.id = db_id
        self.liked = liked
        self.name = name
        self.s_number = s_number
        self.user_id = user_id

    def __str__(self):
        return f'''
            User(age={self.age}, bio={self.bio}, birth_date={self.birth_date}, city={self.city}, created={self.created}, 
            distance={self.distance}, id={self.id}, liked={self.liked},, name={self.name},
            photos={[str(photo) for photo in self.photos]} s_number={self.s_number}, 'user_id={self.user_id})
        '''


class ScheduledDao:
    id: int

    def __init__(self, db_id: int):
        self.id = db_id

    def __str__(self):
        return f'Scheduled(user={self.id})'


class RemainingLikesDao:
    likes_remaining: int
    rate_limited_until: datetime

    def __init__(self, likes_remaining: int, rate_limited_until: int = None):
        self.likes_remaining = likes_remaining
        if rate_limited_until is None:
            self.rate_limited_until = datetime.datetime.now()
        else:
            # convert to seconds from millis
            seconds = rate_limited_until // 1000
            local_datetime: datetime = datetime.datetime.utcfromtimestamp(seconds) + datetime.timedelta(hours=2)
            self.rate_limited_until = local_datetime.strftime('%d %B %Y, %H:%M')

    def to_dict(self):
        return {'likes_remaining': self.likes_remaining, 'rate_limited_until': self.rate_limited_until}
