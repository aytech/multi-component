import os
import time

from db.PostgresStorage import PostgresStorage
from utilities.TinderProcessor import TinderProcessor

AUTH_TOKEN = os.environ['AUTH_TOKEN']
COLLECT_USER_LIMIT = int(os.environ.get('COLLECT_USER_LIMIT', default=10))
DAILY_LIKES_LIMIT = int(os.environ.get('DAILY_LIKES_LIMIT', default=10))
USER_TO_LIKE = os.environ.get('USER_TO_LIKE', default=None)

if __name__ == '__main__':
    time.sleep(3)  # wait for DB to spin up
    storage_session = PostgresStorage()
    processor = TinderProcessor(storage=storage_session, auth_token=AUTH_TOKEN)

    while True:
        processor.like_teaser_profiles(other_teaser_name=USER_TO_LIKE)
        processor.process_daily_likes(limit=DAILY_LIKES_LIMIT)
        processor.collect_profiles(limit=COLLECT_USER_LIMIT)
        time.sleep(3600)
