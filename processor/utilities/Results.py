from typing import Optional

from db.dao import UserDao, PhotoDao, UserTeaserDao, RemainingLikesDao, LikesResponseDao
from utilities.DateProcessor import DateProcessor
from utilities.errors.GenericError import GenericError
from utilities.errors.TimeoutReceivedError import TimeoutReceivedError


class Results:

    @staticmethod
    def process_json_data(json_data=None) -> dict:
        if json_data is None:
            raise GenericError(reason='Response data is null')
        if 'data' not in json_data:
            raise GenericError(reason=json_data)
        if 'timeout' in json_data['data']:
            raise TimeoutReceivedError(reason=json_data)
        return json_data['data']

    @staticmethod
    def user_list(json_data=None) -> list[UserDao]:
        data = Results.process_json_data(json_data=json_data)
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
                liked=False,
                name=result['user']['name'],
                s_number=result['s_number'],
                user_id=result['user']['_id'])
            new_user.bio = result['user']['bio']
            new_user.set_distance(result['distance_mi'])
            if 'birth_date' in result['user']:
                new_user.age = DateProcessor.get_user_age(birth_date=result['user']['birth_date'])
                new_user.birth_date = DateProcessor.get_user_birth_date(birth_date=result['user']['birth_date'])
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
    def teaser_user(json_data=None) -> Optional[UserTeaserDao]:
        data = Results.process_json_data(json_data=json_data)
        if 'recently_active' not in data:
            return None
        if 'name' not in data['recently_active']:
            return None
        return UserTeaserDao(name=data['recently_active']['name'])

    @staticmethod
    def remaining_likes(json_data=None) -> Optional[RemainingLikesDao]:
        data = Results.process_json_data(json_data=json_data)
        if 'likes' not in data:
            return None
        if 'rate_limited_until' not in data['likes']:
            return RemainingLikesDao(likes_remaining=data['likes']['likes_remaining'])
        return RemainingLikesDao(likes_remaining=data['likes']['likes_remaining'],
                                 rate_limited_until=data['likes']['rate_limited_until'])

    '''
        {
            "status":200,
            "match":false,
            "likes_remaining":0
        }
    '''

    @staticmethod
    def like_result(json_data=None) -> LikesResponseDao:
        if json_data is None:
            raise GenericError(reason='Response data is null')
        response = LikesResponseDao()
        if 'likes_remaining' in json_data:
            response.likes_remaining = json_data['likes_remaining']
        if 'match' in json_data:
            response.match = json_data['match']
        if 'status' in json_data:
            response.status = json_data['status']
        return response
