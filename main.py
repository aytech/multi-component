import os
import time

import requests
from requests import JSONDecodeError

from db.PostgresStorage import PostgresStorage
from __models.Results import Results
from models import User

AUTH_TOKEN = os.environ['AUTH_TOKEN']
NAME_TO_LIKE = os.environ['NAME_TO_LIKE']
PROFILES_TO_LIKE = int(os.environ.get('PROFILES_TO_LIKE', default=10))
PROFILES_TO_CHECK = int(os.environ.get('PROFILES_TO_CHECK', default=10))  # how many profiles to check to find like


def wait_for_new_poll(previous_data, _registry: PostgresStorage):
    if 'data' in previous_data:
        if 'timeout' in previous_data['data']:
            timeout_seconds = int(previous_data['data']['timeout'] / 1000)
            _registry.add_message('Sleeping for %s seconds' % timeout_seconds)
            time.sleep(timeout_seconds)


def get_request_headers():
    return {'X-Auth-Token': AUTH_TOKEN}


def get_batch_data(_registry: PostgresStorage) -> Results:
    list_url = 'https://api.gotinder.com/v2/recs/core'
    response = requests.get(list_url, headers=get_request_headers())
    try:
        data = response.json()
        if 'data' in data and 'results' in data['data']:
            return Results(response.json())
        else:
            wait_for_new_poll(data, _registry=_registry)
            return Results()
    except JSONDecodeError as e:
        if response.status_code == 401:
            _registry.add_message('Failed to fetch batch data, not authorized')
        else:
            _registry.add_message('Failed to fetch batch data, reason: %s' % e)
        exit(1)


def send_like(user: User, _registry: PostgresStorage) -> None:
    payload = {
        's_number': user.s_number,
        'liked_content_id': user.photos[0].id,
        'liked_content_type': 'photo'
    }
    like_url = 'https://api.gotinder.com/like/'
    result = requests.post(like_url + user.user_id, headers=get_request_headers(), json=payload)
    _registry.add_message('User %s - %s is liked with status %s' % (user.name, user.id, result.json()['status']))


def send_pass(user: User, _registry: PostgresStorage) -> None:
    pass_url = 'https://api.gotinder.com/pass/'
    params = {'s_number': user.s_number}

    response = requests.get(pass_url + user.user_id, headers=get_request_headers(), params=params)
    _registry.add_message('User %s is passed with status code %s' % (user.name, response.json()['status']))


def process_next_like(_registry: PostgresStorage):
    profiles_checked = 0

    # while True:

    time.sleep(1)  # wait before getting next batch

    if profiles_checked >= PROFILES_TO_CHECK:
        return False

    results = get_batch_data(_registry=_registry)

    for user in results.users:
        print(user)
        print('ID: ', _registry.get_user(user_id=user.id))

        if profiles_checked >= PROFILES_TO_CHECK:
            return False
        time.sleep(1)  # sleep before liking or passing

        if NAME_TO_LIKE == user.name and len(user.photos) > 0:
            if _registry.get_user(user_id=user.id) is not None:
                _registry.add_message('User %s (%s) is already liked!!!' % (user.name, user.id))
            else:
                send_like(user=user, _registry=_registry)
                _registry.add_user(user=user)
                _registry.add_message('Next like %s is found and liked!!!' % user.name)
        else:
            if _registry.get_user(user_id=user.id):
                _registry.add_message('User %s (%s) is already passed!!!' % (user.name, user.id))
            else:
                send_pass(user=user, _registry=_registry)
                _registry.add_user(user=user)
                _registry.add_message(
                    'User %s does not match with %s, continue polling...' % (user.name, NAME_TO_LIKE))
        profiles_checked += 1


def process_local_likes(_registry: PostgresStorage):
    profiles_liked = 0

    while True:

        time.sleep(1)  # wait before getting next batch

        if profiles_liked >= PROFILES_TO_LIKE:
            return False

        results = get_batch_data(_registry=_registry)

        for user in results.users:

            if profiles_liked >= PROFILES_TO_LIKE:
                return False

            time.sleep(1)  # sleep before liking

            if user.city in ('Praha', 'Hlavní město Praha', 'Прага', 'Prague', 'Beroun',):
                if _registry.get_user(user.id):
                    _registry.add_message('User %s (%s) is already liked!!!' % (user.name, user.id))
                else:
                    send_like(user=user, _registry=_registry)
                    _registry.add_user(user=user)
                    profiles_liked += 1
            else:
                if _registry.get_user(user.id):
                    _registry.add_message('User %s (%s) is already passed!!!' % (user.name, user.id))
                else:
                    send_pass(user=user, _registry=_registry)
                    _registry.add_user(user=user)
                    _registry.add_message('Passing user %s, since is in %s' % (user.name, user.city))


if __name__ == '__main__':
    storage_session = PostgresStorage()

    if not process_next_like(_registry=storage_session):
        storage_session.add_message('Next like not found, proceed to like local profiles...')
        process_local_likes(_registry=storage_session)
