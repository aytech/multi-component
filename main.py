import os

from db.PostgresStorage import PostgresStorage
from utilities.TinderProcessor import TinderProcessor

AUTH_TOKEN = os.environ['AUTH_TOKEN']
NAME_TO_LIKE = os.environ['NAME_TO_LIKE']
PROFILES_TO_LIKE = int(os.environ.get('PROFILES_TO_LIKE', default=10))
PROFILES_TO_CHECK = int(os.environ.get('PROFILES_TO_CHECK', default=10))  # how many profiles to check to find like

if __name__ == '__main__':
    storage_session = PostgresStorage()
    processor = TinderProcessor(storage=storage_session, auth_token=AUTH_TOKEN)

    storage_session.add_message(message='Processing %s as next like with limit %s, also %s profiles to like.' % (
        NAME_TO_LIKE, PROFILES_TO_CHECK, PROFILES_TO_LIKE))

    processor.process_next_like(name_to_like=NAME_TO_LIKE, profiles_to_check=PROFILES_TO_CHECK)
    processor.process_local_likes(profiles_to_like=PROFILES_TO_LIKE)
