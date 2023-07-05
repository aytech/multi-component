import time

from utilities.MainProcessor import MainProcessor


def get_processor():
    try:
        return MainProcessor()
    except Exception as e:
        print('Failed to initialize service, reason: %s' % e)
        time.sleep(2)
        return get_processor()


if __name__ == '__main__':

    processor = get_processor()

    while True:
        processor.collect_teaser()
        processor.process_likes()
        processor.collect_profiles()

        time.sleep(3600)  # wait for an hour
