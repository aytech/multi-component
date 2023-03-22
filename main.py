import os
import sys

from db.PostgresStorage import PostgresStorage
from utilities.TinderProcessor import TinderProcessor

AUTH_TOKEN = os.environ['AUTH_TOKEN']
NAME_TO_FIND = os.environ['NAME_TO_FIND']
BATCH_LIKE_LIMIT = int(os.environ.get('PROFILES_TO_LIKE', default=10))
BATCH_FIND_LIMIT = int(os.environ.get('PROFILES_TO_CHECK', default=10))

if __name__ == '__main__':
    args = sys.argv[1:]
    storage_session = PostgresStorage()
    processor = TinderProcessor(storage=storage_session, auth_token=AUTH_TOKEN)

    if len(args) >= 1 and args[0] == 'batch_find':
        processor.process_batch_scan(target_profile_name=NAME_TO_FIND, limit=BATCH_FIND_LIMIT)
    if len(args) >= 2 and args[1] == 'batch_like':
        processor.process_batch_likes(limit=BATCH_LIKE_LIMIT)
    if len(args) >= 3 and args[2] == 'like_profile':
        print('Processing like profile, to be implemented...')
