import json
from typing import Optional

from utilities.RemainingLikesDao import RemainingLikesDao


class Results:

    @staticmethod
    def process_json_data(json_data=None) -> Optional[dict]:
        if json_data is None:
            return None
        if 'data' not in json_data:
            return None
        if 'timeout' in json_data['data']:
            return None
        data = json_data['data']
        if 'likes' not in data:
            return None
        return data['likes']

    @staticmethod
    def remaining_likes(response_data=None) -> Optional[RemainingLikesDao]:
        if response_data is None or response_data == '':
            return RemainingLikesDao(likes_remaining=0)
        likes: dict = Results.process_json_data(json_data=json.loads(response_data))
        if likes is None:
            return RemainingLikesDao(likes_remaining=0)
        if 'rate_limited_until' not in likes:
            return RemainingLikesDao(likes_remaining=likes['likes_remaining'])
        return RemainingLikesDao(likes_remaining=likes['likes_remaining'],
                                 rate_limited_until=likes['rate_limited_until'])
