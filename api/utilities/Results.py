from typing import Optional

from db.dao import RemainingLikesDao
from errors.GenericError import GenericError
from errors.TimeoutReceivedError import TimeoutReceivedError


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
    def remaining_likes(json_data=None) -> Optional[RemainingLikesDao]:
        data = Results.process_json_data(json_data=json_data)
        if 'likes' not in data:
            return None
        if 'rate_limited_until' not in data['likes']:
            return RemainingLikesDao(likes_remaining=data['likes']['likes_remaining'])
        return RemainingLikesDao(likes_remaining=data['likes']['likes_remaining'],
                                 rate_limited_until=data['likes']['rate_limited_until'])
