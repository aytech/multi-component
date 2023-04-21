import os
import time

from db.PostgresStorage import PostgresStorage
from db.dao import RemainingLikesDao
from utilities.MainProcessor import MainProcessor

AUTH_TOKEN = os.environ.get('AUTH_TOKEN', default='')
BASE_URL = os.environ.get('BASE_URL', default='')

if __name__ == '__main__':
    time.sleep(3)  # wait for DB to spin up
    storage_session = PostgresStorage()
    processor = MainProcessor(storage=storage_session, auth_token=AUTH_TOKEN, base_url=BASE_URL)

    while True:
        remaining_likes: RemainingLikesDao = processor.remaining_likes()
        if remaining_likes.likes_remaining < 1:
            storage_session.add_message('No likes remaining till %s' % remaining_likes.rate_limited_until)
        else:
            storage_session.add_message('%s likes remaining' % remaining_likes.likes_remaining)
            processor.process_daily_likes(limit=remaining_likes.likes_remaining)

        storage_session.add_message('Processing collecting profiles')
        processor.collect_profiles()

        time.sleep(3600)  # wait for an hour
