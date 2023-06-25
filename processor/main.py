import time

from utilities.MainProcessor import MainProcessor

if __name__ == '__main__':
    processor = MainProcessor()

    while True:
        processor.collect_teaser()
        processor.process_likes()
        processor.collect_profiles()

        time.sleep(3600)  # wait for an hour
