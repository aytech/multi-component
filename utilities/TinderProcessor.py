import time
from typing import Optional

import requests

from db.PostgresStorage import PostgresStorage
from db.dao import UserDao, UserTeaserDao
from utilities.Results import Results
from utilities.errors.BaseError import BaseError


class TinderProcessor:
    base_url: str = 'https://api.gotinder.com'
    request_headers: dict
    storage: PostgresStorage

    def get_batch_profile_data(self) -> list[UserDao]:
        self.storage.add_message('Retrieving batch profile data')
        response = requests.get('%s/v2/recs/core' % self.base_url, headers=self.request_headers)
        return Results.user_list(raw_data=response)

    def get_teaser_profile(self) -> Optional[UserTeaserDao]:
        self.storage.add_message('Retrieving teaser user profile')
        response = requests.get('%s/v2/fast-match/teaser?type=recently-active' % self.base_url,
                                headers=self.request_headers)
        return Results.teaser_user(raw_data=response)

    def collect_profiles(self):

        while True:

            time.sleep(3)  # wait before getting next batch

            try:
                results: list[UserDao] = self.get_batch_profile_data()
            except BaseError as e:
                self.storage.add_message(message=e.message, persist=True)
                return

            for user in results:

                if self.storage.get_user(user_id=user.user_id) is None:
                    self.storage.add_user(user=user)
                    message = 'User %s (%s) added to the system'
                else:
                    message = 'User %s (%s) is already in the system'
                self.storage.add_message(message % (user.name, user.user_id))

    def process_daily_likes(self):

        profiles_liked = 0

        while True:

            time.sleep(3)  # wait before getting next batch

            try:
                results: list[UserDao] = self.get_batch_profile_data()
            except BaseError as e:
                self.storage.add_message(message=e.message, persist=True)
                return

            for user in results:

                time.sleep(1)  # wait between likes

                if self.like_user(user=user):
                    profiles_liked += 1
                    self.storage.add_message('Liked %s profiles so far...' % profiles_liked, persist=True)
                else:
                    self.pass_user(user=user, reason='user is in %s' % user.city)

    def check_teaser_profile(self) -> None:
        try:
            teaser_profile: Optional[UserTeaserDao] = self.get_teaser_profile()
        except BaseError as e:
            self.storage.add_message(message=e.message)
            return

        if teaser_profile is not None:
            local_profiles: list[UserDao] = self.storage.get_users_by_name(name=teaser_profile.name)
            if len(local_profiles) == 0:
                message: str = 'Teaser profile(s) for %s not found locally, exiting...'
                self.storage.add_message(message % teaser_profile.name)
                return
            else:
                message: str = '%s teaser profile(s) for %s found locally, sending like(s)...'
                self.storage.add_message(message % teaser_profile.name)
                for profile in local_profiles:
                    self.like_user(user=profile, force=True)

    def like_user(self, user: UserDao, force: bool = False) -> bool:
        if force is False and self.storage.get_user(user_id=user.user_id) is not None:
            self.storage.add_message('User %s (%s) is already liked!!!' % (user.name, user.user_id))
            return False
        else:
            response = requests.post('%s/like/%s' % (self.base_url, user.user_id), headers=self.request_headers, json={
                's_number': user.s_number,
                'liked_content_id': user.photos[0].photo_id,
                'liked_content_type': 'photo'
            })
            if force is False:
                self.storage.add_user(user=user)
            message = 'User %s (%s) is liked with status %s'
            response_status = response.json()['status']
            self.storage.add_message(message=message % (user.name, user.user_id, response_status), persist=True)
            return True

    def pass_user(self, user: UserDao, reason: str) -> bool:
        if self.storage.get_user(user_id=user.user_id):
            self.storage.add_message('User %s (%s) is already passed!!!' % (user.name, user.user_id))
            return False
        else:
            response = requests.get('%s/pass/%s' % (self.base_url, user.user_id), headers=self.request_headers,
                                    params={'s_number': user.s_number})
            self.storage.add_user(user=user)
            message = 'User %s (%s) is passed with status code %s, reason: %s'
            response_status = response.json()['status']
            self.storage.add_message(message=message % (user.name, user.user_id, response_status, reason), persist=True)
            return True

    def __init__(self, storage: PostgresStorage, auth_token: str):
        self.storage = storage
        self.request_headers = {'X-Auth-Token': auth_token, 'Host': 'api.gotinder.com'}
