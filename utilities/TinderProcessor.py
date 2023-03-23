import time

import requests
from requests import JSONDecodeError

from db.PostgresStorage import PostgresStorage
from db.dao import UserDao
from utilities.CommunicationError import CommunicationError
from utilities.Results import Results


class TinderProcessor:
    cities_to_match = ('Praha', 'Hlavní město Praha', 'Прага', 'Prague', 'Beroun',)
    like_url: str = 'https://api.gotinder.com/like/'
    pass_url: str = 'https://api.gotinder.com/pass/'
    request_headers: dict
    storage: PostgresStorage

    @staticmethod
    def is_timeout(response_data) -> bool:
        return 'data' in response_data and 'timeout' in response_data['data']

    def get_batch_profile_data(self) -> Results:
        list_url = 'https://api.gotinder.com/v2/recs/core'
        self.storage.add_message('Retrieving batch profile data')
        response = requests.get(list_url, headers=self.request_headers)
        try:
            data = response.json()
            if 'data' in data and 'results' in data['data']:
                return Results(response.json())
            elif self.is_timeout(response_data=data):
                raise CommunicationError(message='Timeout received while fetching profile data: %s' % data)
            else:
                raise CommunicationError(message='Unknown error occurred while fetching profile data: %s' % data)
        except JSONDecodeError as e:
            if response.status_code == 401:
                message = 'Failed to fetch batch data, not authorized'
            else:
                message = 'Failed to fetch batch data, reason: %s' % e
            raise CommunicationError(message=message)

    def process_batch_scan(self, target_profile_name: str, limit: int = 10):

        profiles_scanned = 0

        while True:

            time.sleep(1)  # wait before getting next batch

            if profiles_scanned >= limit:
                message = 'Terminating next like process, as already checked %s profiles out of %s'
                self.storage.add_message(message % (profiles_scanned, limit))
                return

            try:
                results = self.get_batch_profile_data()
            except CommunicationError as e:
                self.storage.add_message('Terminating batch scan, reason: %s' % e.message)
                return

            for user in results.users:

                self.storage.add_message('Processed %s out of %s profiles so far...' % (profiles_scanned, limit))

                if profiles_scanned >= limit:
                    message = 'Terminating next like process, as already checked %s profiles out of %s'
                    self.storage.add_message(message % (profiles_scanned, limit))
                    return
                time.sleep(1)  # sleep before liking or passing

                if target_profile_name == user.name and len(user.photos) > 0:
                    self.like_user(user=user)
                    message = 'Terminating next like process, as desired profile (%s) is found'
                    self.storage.add_message(message % target_profile_name)
                    return
                else:
                    if self.pass_user(user=user, reason='name does not match %s' % target_profile_name):
                        profiles_scanned += 1

    def process_batch_likes(self, limit: int = 10):

        profiles_scanned = 0
        terminate_message = 'Terminating like process, as already liked %s profiles out of %s'

        while True:

            time.sleep(1)  # wait before getting next batch

            if profiles_scanned >= limit:
                self.storage.add_message(terminate_message % (profiles_scanned, limit))
                return

            try:
                results = self.get_batch_profile_data()
            except CommunicationError as e:
                self.storage.add_message('Terminating batch likes, reason: %s' % e.message)
                return

            for user in results.users:

                self.storage.add_message('Liked %s out of %s profiles so far...' % (profiles_scanned, limit))

                if profiles_scanned >= limit:
                    self.storage.add_message(terminate_message % (profiles_scanned, limit))
                    return

                time.sleep(1)  # sleep before liking

                if user.city in self.cities_to_match:
                    if self.like_user(user=user):
                        profiles_scanned += 1
                else:
                    self.pass_user(user=user, reason='user is in %s' % user.city)

    def like_profile(self, user_name: str) -> None:
        for user in self.storage.get_users_by_name(user_name=user_name):
            self.storage.add_message('Processing explicit like for user %s (%s)' % (user.name, user.user_id))
            self.like_user(user=user, force=True)

    def like_user(self, user: UserDao, force: bool = False) -> bool:
        if force is False and self.storage.get_user(user_id=user.user_id) is not None:
            self.storage.add_message('User %s (%s) is already liked!!!' % (user.name, user.user_id))
            return False
        else:
            response = requests.post(self.like_url + user.user_id, headers=self.request_headers, json={
                's_number': user.s_number,
                'liked_content_id': user.photos[0].photo_id,
                'liked_content_type': 'photo'
            })
            if force is False:
                self.storage.add_user(user=user)
            message = 'User %s (%s) is liked with status %s'
            self.storage.add_message(message % (user.name, user.user_id, response.json()['status']))
            return True

    def pass_user(self, user: UserDao, reason: str) -> bool:
        if self.storage.get_user(user_id=user.user_id):
            self.storage.add_message('User %s (%s) is already passed!!!' % (user.name, user.user_id))
            return False
        else:
            response = requests.get(self.pass_url + user.user_id, headers=self.request_headers,
                                    params={'s_number': user.s_number})
            self.storage.add_user(user=user)
            message = 'User %s (%s) is passed with status code %s, reason: %s'
            self.storage.add_message(message % (user.name, user.user_id, response.json()['status'], reason))
            return True

    def __init__(self, storage: PostgresStorage, auth_token: str):
        self.storage = storage
        self.request_headers = {'X-Auth-Token': auth_token}
