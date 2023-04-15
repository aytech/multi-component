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
    liked: bool
    name: str
    photos: list[PhotoDao]
    s_number: int
    user_id: str

    def __init__(self, liked: bool, name: str, s_number: int, user_id: str, city: Optional[str] = None):
        self.city = city
        self.liked = liked
        self.name = name
        self.s_number = s_number
        self.user_id = user_id

    def __str__(self):
        return f'''
            User(city={self.city!r}, liked={self.liked!r},, name={self.name!r},
            photos={[str(photo) for photo in self.photos]} s_number={self.s_number!r}, 'user_id={self.user_id})
        '''


class UserTeaserDao:
    name: str

    def __init__(self, name: str):
        self.name = name
