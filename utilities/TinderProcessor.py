import time

import requests
from requests import JSONDecodeError

from db.PostgresStorage import PostgresStorage
from db.dao import UserDao
from utilities.Results import Results


class TinderProcessor:
    cities_to_match = ('Praha', 'Hlavní město Praha', 'Прага', 'Prague', 'Beroun',)
    like_url: str = 'https://api.gotinder.com/like/'
    pass_url: str = 'https://api.gotinder.com/pass/'
    request_headers: dict
    storage: PostgresStorage

    def get_batch_profile_data(self) -> Results:
        list_url = 'https://api.gotinder.com/v2/recs/core'
        response = requests.get(list_url, headers=self.request_headers)
        try:
            data = response.json()
            if 'data' in data and 'results' in data['data']:
                return Results(response.json())
            else:
                self.wait_for_new_poll(data)
        except JSONDecodeError as e:
            if response.status_code == 401:
                self.storage.add_message('Failed to fetch batch data, not authorized')
            else:
                self.storage.add_message('Failed to fetch batch data, reason: %s' % e)
        return Results()

    def process_next_like(self, name_to_like, profiles_to_check: int = 10):

        profiles_checked = 0

        while True:

            time.sleep(1)  # wait before getting next batch

            if profiles_checked >= profiles_to_check:
                return

            results = self.get_batch_profile_data()

            for user in results.users:

                if profiles_checked >= profiles_to_check:
                    return
                time.sleep(1)  # sleep before liking or passing

                if name_to_like == user.name and len(user.photos) > 0:
                    self.like_user(user=user)
                else:
                    self.pass_user(user=user, reason='name does not match %s' % name_to_like)
                profiles_checked += 1

    def process_local_likes(self, profiles_to_like: int = 10):
        profiles_liked = 0

        while True:

            time.sleep(1)  # wait before getting next batch

            if profiles_liked >= profiles_to_like:
                return

            results = self.get_batch_profile_data()

            for user in results.users:

                if profiles_liked >= profiles_to_like:
                    return

                time.sleep(1)  # sleep before liking

                if user.city in self.cities_to_match:
                    self.like_user(user=user)
                    profiles_liked += 1
                else:
                    self.pass_user(user=user, reason='user is in %s' % user.city)

    def like_user(self, user: UserDao):
        if self.storage.get_user(user_id=user.user_id) is not None:
            self.storage.add_message('User %s (%s) is already liked!!!' % (user.name, user.user_id))
        else:
            response = requests.post(self.like_url + user.user_id, headers=self.request_headers, json={
                's_number': user.s_number,
                'liked_content_id': user.photos[0].photo_id,
                'liked_content_type': 'photo'
            })
            self.storage.add_user(user=user)
            self.storage.add_message(
                'User %s - %s is liked with status %s' % (user.name, user.user_id, response.json()['status']))

    def pass_user(self, user: UserDao, reason: str):
        if self.storage.get_user(user_id=user.user_id):
            self.storage.add_message('User %s (%s) is already passed!!!' % (user.name, user.user_id))
        else:
            response = requests.get(self.pass_url + user.user_id, headers=self.request_headers,
                                    params={'s_number': user.s_number})
            self.storage.add_user(user=user)
            self.storage.add_message(
                'User %s is passed with status code %s, reason: %s' % (user.name, response.json()['status'], reason))

    def wait_for_new_poll(self, response_data):
        if 'data' in response_data:
            if 'timeout' in response_data['data']:
                timeout_seconds = int(response_data['data']['timeout'] / 1000)
                self.storage.add_message('Sleeping for %s seconds' % timeout_seconds)
                time.sleep(timeout_seconds)

    def __init__(self, storage: PostgresStorage, auth_token: str):
        self.storage = storage
        self.request_headers = {'X-Auth-Token': auth_token}
