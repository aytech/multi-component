from typing import Optional

from requests import JSONDecodeError

from db.dao import UserDao, PhotoDao, UserTeaserDao
from utilities.errors.AuthorisationError import AuthorisationError
from utilities.errors.GenericError import GenericError
from utilities.errors.TimeoutReceivedError import TimeoutReceivedError


class Results:

    @staticmethod
    def process_raw_data(raw_data=None) -> dict:
        try:
            data = raw_data.json()
        except JSONDecodeError as e:
            if raw_data.status_code == 401:
                raise AuthorisationError()
            else:
                raise GenericError(reason=e.response)
        if data is None:
            raise GenericError(reason='Response data is null')
        if 'data' not in data:
            raise GenericError(reason=data)
        if 'timeout' in data['data']:
            raise TimeoutReceivedError(reason=data)
        return data['data']

    @staticmethod
    def user_list(raw_data=None) -> list[UserDao]:
        data = Results.process_raw_data(raw_data=raw_data)
        users: list[UserDao] = []
        if 'results' not in data:
            return users
        for result in data['results']:
            if 'type' not in result:
                return users
            if result['type'] != 'user':
                return users
            if 'user' not in result:
                return users
            new_user = UserDao(
                name=result['user']['name'],
                s_number=result['s_number'],
                user_id=result['user']['_id'])
            if 'city' in result['user']:
                new_user.city = result['user']['city']['name']
            if 'photos' in result['user']:
                photos = []
                for photo in result['user']['photos']:
                    photos.append(PhotoDao(
                        photo_id=photo['id'],
                        url=photo['url']
                    ))
                new_user.photos = photos
            users.append(new_user)
        return users

    @staticmethod
    def teaser_user(raw_data=None) -> Optional[UserTeaserDao]:
        data = Results.process_raw_data(raw_data=raw_data)
        if 'recently_active' not in data:
            return None
        if 'name' not in data['recently_active']:
            return None
        return UserTeaserDao(name=data['recently_active']['name'])
