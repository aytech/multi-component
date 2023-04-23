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
        if remaining_likes.likes_remaining > 50:  # leave 50 for manual likes
            processor.process_daily_likes(limit=10)

        processor.collect_teaser()
        processor.collect_profiles()

        time.sleep(3600)  # wait for an hour
