import json
import math
import os
import shutil
import time
from random import random
from typing import Optional

import certifi
import requests
import urllib3

from db.PostgresStorage import PostgresStorage
from db.dao import UserDao, UserTeaserDao, RemainingLikesDao
from utilities.LogLevel import LogLevel
from utilities.Results import Results
from utilities.errors.AuthorizationError import AuthorizationError
from utilities.errors.BaseError import BaseError


class MainProcessor:
    base_url: str
    pool_manager: urllib3.PoolManager
    request_headers: dict
    storage: PostgresStorage

    def get_batch_profile_data(self) -> list[UserDao]:
        time.sleep(5)  # wait before getting next batch, as it will be invoked in loop
        url: str = '%s/v2/recs/core' % self.base_url
        request = self.pool_manager.request(method='GET', url=url, headers=self.request_headers)
        if request.status == requests.status_codes.codes.unauthorized:
            raise AuthorizationError(message='while fetching profiles data')
        return Results.user_list(json_data=json.loads(request.data.decode('utf-8')))

    def get_teaser_profile(self) -> Optional[UserTeaserDao]:
        url: str = '%s/v2/fast-match/teaser?type=recently-active' % self.base_url
        request = self.pool_manager.request(method='GET', url=url, headers=self.request_headers)
        if request.status == requests.status_codes.codes.unauthorized:
            raise AuthorizationError(message='while fetching teaser profile')
        return Results.teaser_user(json_data=json.loads(request.data.decode('utf-8')))

    def pass_user(self, user: UserDao) -> None:
        request = self.pool_manager.request(method='GET', url='%s/pass/%s' % (self.base_url, user.user_id),
                                            headers=self.request_headers, fields={'s_number': user.s_number})
        message = 'User %s (%s) is passed with status code %s'
        self.storage.add_message(message=message % (user.name, user.user_id, request.status))

    def like_user(self, user: UserDao) -> bool:
        user_local: Optional[UserDao] = self.storage.get_user_by_user_id(user_id=user.user_id)

        if user_local is not None and user_local.liked is True:
            self.storage.add_message(message='User %s (%s) is already liked, renewing...' % (user.name, user.user_id))
            self.storage.renew_user_image_urls(user_dao=user_local)
            return False

        if user_local is None:
            self.storage.add_user(user=user)

        url: str = '%s/like/%s' % (self.base_url, user.user_id)
        request = self.pool_manager.request(method='POST', url=url, headers=self.request_headers, body=json.dumps({
            's_number': user.s_number,
            'liked_content_id': user.photos[0].photo_id,
            'liked_content_type': 'photo'
        }))
        message = 'User %s (%s) is liked with status %s'
        self.storage.add_message(message=message % (user.name, user.user_id, request.status))
        self.storage.update_user_like_status(user_id=user.user_id, status=True)
        return True

    def fetch_remaining_likes(self) -> RemainingLikesDao:
        url: str = '%s/v2/profile?include=likes' % self.base_url
        request = self.pool_manager.request(method='GET', url=url, headers=self.request_headers)
        if request.status == requests.status_codes.codes.unauthorized:
            raise AuthorizationError(message='while fetching teaser profile')
        return Results.remaining_likes(json_data=json.loads(request.data.decode('utf-8')))

    def download_images(self, user: UserDao) -> UserDao:
        for photo in user.photos:
            directory_name: str = 'images/%s' % user.user_id
            image_path = '%s/photo_%s.jpg' % (directory_name, math.ceil(random() * 100))
            if not os.path.exists(directory_name):
                os.mkdir(directory_name)
            request = self.pool_manager.request('GET', url=photo.url, preload_content=False)
            with open(image_path, 'wb') as out_file:
                shutil.copyfileobj(request, out_file)
            request.release_conn()
            photo.url = image_path
        return user

    def process_daily_likes(self) -> None:

        remaining_likes_remote: int
        profiles_liked: int = 0

        while True:
            try:
                results: list[UserDao] = self.get_batch_profile_data()
            except BaseError as e:
                self.storage.add_message(message=e.message)
                return

            for user in results:

                time.sleep(1)  # wait between likes
                remaining_likes_remote = self.fetch_remaining_likes().likes_remaining  # this will be either 100 or 0

                if remaining_likes_remote == 0:
                    self.storage.add_message(message='No more likes available, liked %s profiles' % profiles_liked)
                    return

                if self.like_user(user=user):
                    profiles_liked += 1
                    self.storage.add_update_remaining_likes(remaining_likes=(remaining_likes_remote - profiles_liked))

    def collect_profiles(self, limit: int = 100) -> None:

        profiles_collected = 0
        new_profiles = 0

        while True:
            try:
                profiles_batch: list[UserDao] = self.get_batch_profile_data()
            except BaseError as e:
                self.storage.add_message(message=e.message)
                return

            batch_size = len(profiles_batch)

            for index in range(0, batch_size):
                user: UserDao = profiles_batch[index]

                profiles_collected += 1

                if self.storage.get_user(user_id=user.user_id) is None:
                    self.storage.add_user(user=user)
                    message: str = 'User %s (%s) added to the system'
                    self.storage.add_message(message=message % (user.name, user.user_id))
                    new_profiles += 1
                else:
                    self.storage.renew_user_image_urls(user_dao=user)
                    message: str = 'User %s (%s) was renewed'
                    self.storage.add_message(message=message % (user.name, user.user_id))

                if profiles_collected >= limit:
                    message: str = 'Terminating collecting profiles, as limit of %s reached, added %s new users'
                    self.storage.add_message(message=message % (limit, new_profiles))
                    return

    def collect_teaser(self):
        teaser: Optional[UserTeaserDao] = None
        try:
            teaser = self.get_teaser_profile()
        except AuthorizationError:
            self.storage.add_message("Authorization error while fetching teaser profile", LogLevel.WARN)
        if teaser is not None:
            self.storage.add_teaser(teaser=teaser.name)

    def __init__(self, storage: PostgresStorage):
        self.base_url = 'https://%s' % storage.get_base_url()
        self.storage = storage
        self.request_headers = {'X-Auth-Token': storage.get_api_key(), 'Host': storage.get_base_url()}
        self.pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
