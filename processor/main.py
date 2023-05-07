import time

from db.PostgresStorage import PostgresStorage
from utilities.MainProcessor import MainProcessor

if __name__ == '__main__':
    time.sleep(3)  # wait for DB to spin up
    storage_session = PostgresStorage()
    processor = MainProcessor(storage=storage_session)

    while True:
        processor.collect_teaser()
        processor.process_likes()
        processor.collect_profiles()

        time.sleep(3600)  # wait for an hour
