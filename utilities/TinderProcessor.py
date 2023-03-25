import time
from datetime import datetime
from typing import Optional

import requests

from db.PostgresStorage import PostgresStorage
from db.dao import UserDao, UserTeaserDao
from db.models import Settings
from utilities.Results import Results
from utilities.errors.BaseError import BaseError


class TinderProcessor:
    base_url: str = 'https://api.gotinder.com'
    storage: PostgresStorage
    request_headers: dict

    def get_batch_profile_data(self) -> list[UserDao]:
        self.storage.add_message('Retrieving batch profile data...')
        time.sleep(5)  # wait before getting next batch, as it will be invoked in loop
        response = requests.get('%s/v2/recs/core' % self.base_url, headers=self.request_headers)
        return Results.user_list(raw_data=response)

    def get_teaser_profile(self) -> Optional[UserTeaserDao]:
        self.storage.add_message('Retrieving teaser user profile')
        response = requests.get('%s/v2/fast-match/teaser?type=recently-active' % self.base_url,
                                headers=self.request_headers)
        return Results.teaser_user(raw_data=response)

    def collect_profiles(self, limit: int = 10):

        profiles_added = 0
        profiles_missed = 0

        while True:
            try:
                results: list[UserDao] = self.get_batch_profile_data()
            except BaseError as e:
                self.storage.add_message(message=e.message, persist=True)
                return

            for user in results:
                if self.storage.get_user(user_id=user.user_id) is None:
                    self.storage.add_user(user=user)
                    message = 'User %s (%s) added to the system'
                    profiles_added += 1
                else:
                    message = 'User %s (%s) is already in the system'
                    profiles_missed += 1
                self.storage.add_message(message % (user.name, user.user_id))

            if profiles_missed >= limit:
                self.storage.add_message(message='Terminating collecting profiles, as predefined limit reached')
                return

    def process_daily_likes(self, limit: int = 10) -> None:

        profiles_liked = 0
        profiles_missed = 0

        last_run_record: Optional[Settings] = self.storage.get_daily_run_setting()

        if last_run_record is not None:
            last_run_time = datetime.strptime(last_run_record.value, '%Y-%m-%d %H:%M:%S.%f')
            current_time = datetime.now()
            hours_since_last_run: int = (current_time - last_run_time).seconds // 3600
            if hours_since_last_run < 12:
                message = 'Only %s hours passed since last likes run, skipping...'
                self.storage.add_message(message % hours_since_last_run)
                return

        while True:
            try:
                results: list[UserDao] = self.get_batch_profile_data()
            except BaseError as e:
                self.storage.add_message(message=e.message, persist=True)
                return

            for user in results:
                time.sleep(1)  # wait between likes
                if self.like_user(user=user):
                    profiles_liked += 1
                    profiles_missed = 0  # reset missed, the limit should only apply on consecutive misses
                    self.storage.add_message('Liked %s profiles so far...' % profiles_liked, persist=True)
                else:
                    profiles_missed += 1

            # Looks like Tinder API stops giving new profiles when out of likes, so should be limited
            if profiles_missed >= limit:
                self.storage.add_message(message='Terminating daily likes, as likely run out of likes')
                self.storage.record_daily_like_run()
                return

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
