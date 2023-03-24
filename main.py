import os
import sys

from db.PostgresStorage import PostgresStorage
from utilities.TinderProcessor import TinderProcessor

AUTH_TOKEN = os.environ['AUTH_TOKEN']

if __name__ == '__main__':
    args = sys.argv[1:]
    storage_session = PostgresStorage()
    processor = TinderProcessor(storage=storage_session, auth_token=AUTH_TOKEN)

    processor.check_teaser_profile()
    processor.process_daily_likes()
    processor.collect_profiles()
