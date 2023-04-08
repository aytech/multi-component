import time
from typing import Optional

import requests

from db.PostgresStorage import PostgresStorage
from db.dao import UserDao, UserTeaserDao
from db.models import Settings
from utilities.DateProcessor import DateProcessor
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

    def are_likes_exhausted(self) -> bool:
        last_run_record: Optional[Settings] = self.storage.get_daily_run_setting()

        if last_run_record is not None:
            hours_since_last_run = DateProcessor.hours_passed(from_date=last_run_record.value)
            if hours_since_last_run >= 12:
                message: str = '%s hours passed since last run, continuing...'
                self.storage.add_message(message=message % hours_since_last_run, persist=True)
                return False
            else:
                message: str = 'Only %s hours passed since last likes run, skipping...'
                self.storage.add_message(message=message % hours_since_last_run, persist=True)
                return True
        return False  # likes not exhausted if setting is not found

    def collect_profiles(self, limit: int = 10) -> None:

        profiles_added = 0
        profiles_missed = 0
        terminate_message: str = 'Terminating collecting profiles, as limit of %s reached, added %s new users'

        while True:
            try:
                profiles_batch: list[UserDao] = self.get_batch_profile_data()
            except BaseError as e:
                self.storage.add_message(message=e.message, persist=True)
                self.storage.add_message(message=terminate_message % (limit, profiles_added), persist=True)
                return

            batch_size = len(profiles_batch)

            for index in range(0, batch_size):
                user: UserDao = profiles_batch[index]

                if self.storage.get_user(user_id=user.user_id) is None:
                    self.storage.add_user(user=user)
                    profiles_added += 1
                    message: str = 'User %s (%s) added to the system'
                    self.storage.add_message(message=message % (user.name, user.user_id), persist=True)
                else:
                    profiles_missed += 1

                if index == batch_size - 1:  # Pass at least one user in a batch
                    self.pass_user(user=user)

                if profiles_missed >= limit:
                    self.storage.add_message(message=terminate_message % (limit, profiles_added), persist=True)
                    return

    def process_daily_likes(self, limit: int = 10) -> None:

        profiles_liked = 0
        profiles_missed = 0

        if self.are_likes_exhausted():
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
                else:
                    profiles_missed += 1

            # Looks like Tinder API stops giving new profiles when out of likes, so should be limited
            if profiles_missed >= limit:
                self.storage.add_message(message='Terminating daily likes, as likely run out of likes')
                self.storage.record_daily_like_run()
                return

    def like_teaser_profiles(self, other_teaser_name: Optional[str]) -> None:

        if self.are_likes_exhausted():
            return

        try:
            teaser_profile: Optional[UserTeaserDao] = self.get_teaser_profile()
        except BaseError as e:
            self.storage.add_message(message=e.message)
            return

        # Process teaser profile from Tinder first
        if teaser_profile is not None:
            local_profiles: list[UserDao] = self.storage.get_users_by_name(name=teaser_profile.name)
            if len(local_profiles) == 0:
                message: str = 'Teaser profile(s) for %s not found locally, skipping...'
                self.storage.add_message(message=message % teaser_profile.name, persist=False)
            else:
                message: str = '%s teaser profile(s) for %s found locally, sending like(s)...'
                self.storage.add_message(message=message % (len(local_profiles), teaser_profile.name), persist=False)
                for profile in local_profiles:
                    self.like_user(user=profile)

        # Process other teaser profiles as defined
        if other_teaser_name is not None:
            other_profiles: list[UserDao] = self.storage.get_users_by_name(name=other_teaser_name)
            if len(other_profiles) == 0:
                message: str = 'Other teaser profile(s) for %s not found locally, skipping...'
                self.storage.add_message(message=message % other_teaser_name, persist=False)
            else:
                message: str = '%s of other teaser profile(s) for %s found locally, sending like(s)...'
                self.storage.add_message(message=message % (len(other_profiles), other_teaser_name), persist=False)
                for profile in other_profiles:
                    self.like_user(user=profile)

    def like_user(self, user: UserDao) -> bool:
        user_local: Optional[UserDao] = self.storage.get_user_by_user_id(user_id=user.user_id)

        if user_local is not None and user_local.liked is True:
            self.storage.add_message(message='User %s (%s) is already liked!!!' % (user.name, user.user_id))
            return False

        if user_local is None:
            self.storage.add_user(user=user)

        response = requests.post('%s/like/%s' % (self.base_url, user.user_id), headers=self.request_headers, json={
            's_number': user.s_number,
            'liked_content_id': user.photos[0].photo_id,
            'liked_content_type': 'photo'
        })
        message = 'User %s (%s) is liked with status %s'
        response_status = response.json()['status']
        self.storage.add_message(message=message % (user.name, user.user_id, response_status), persist=True)
        self.storage.update_user_like_status(user_id=user.user_id, status=True)
        return True

    def pass_user(self, user: UserDao) -> None:
        response = requests.get('%s/pass/%s' % (self.base_url, user.user_id), headers=self.request_headers,
                                params={'s_number': user.s_number})
        message = 'User %s (%s) is passed with status code %s'
        response_status = response.json()['status']
        self.storage.add_message(message=message % (user.name, user.user_id, response_status), persist=True)

    def __init__(self, storage: PostgresStorage, auth_token: str):
        self.storage = storage
        self.request_headers = {'X-Auth-Token': auth_token, 'Host': 'api.gotinder.com'}
