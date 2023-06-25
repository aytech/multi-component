import json
import os
import time
from typing import Optional

import certifi
import grpc
import requests
import urllib3
import proto.actions_pb2_grpc
import proto.logs_pb2_grpc
import proto.profiles_pb2_grpc
import proto.settings_pb2_grpc
from proto.actions_pb2 import ActionsRequest, LikedStatusRequest, AddProfileRequest, ProfilePhoto, ActionsReply, \
    ActionsPhotoRequest

from proto.empty_pb2 import Empty
from proto.logs_pb2 import LogRequest
from proto.profiles_pb2 import ProfilesReply, ProfileUserIdRequest, ProfileIdReply
from proto.settings_pb2 import AddTeaserRequest, FetchSettingsReply
from db.dao import UserDao, UserTeaserDao, RemainingLikesDao, LikesResponseDao
from utilities.LogLevel import LogLevel
from utilities.Results import Results
from utilities.errors.AuthorizationError import AuthorizationError
from utilities.errors.BaseError import BaseError

grpc_host: str = os.environ.get('GRPC_HOST', default='localhost')
grpc_port: str = os.environ.get('GRPC_PORT', default='50051')


class MainProcessor:
    base_url: str
    pool_manager: urllib3.PoolManager
    request_headers: dict
    logging_context: str = 'PROCESSOR'

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

    def like_user(self, user: ProfilesReply.Profile) -> bool:
        with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
            if user.liked is True:
                message: str = 'User %s (%s) is already liked, skipping...' % (user.name, user.user_id)
                log_stub = proto.logs_pb2_grpc.LogsStub(channel=channel)
                log_stub.LogMessage(
                    LogRequest(message=message, context=self.logging_context, level=LogLevel.INFO.value))
                return False

            url: str = '%s/like/%s' % (self.base_url, user.user_id)
            request = self.pool_manager.request(method='POST', url=url, headers=self.request_headers, body=json.dumps({
                's_number': user.s_number,
                'liked_content_id': user.photos[0].photo_id,
                'liked_content_type': 'photo'
            }))
            response: LikesResponseDao = Results.like_result(json_data=json.loads(request.data.decode('utf-8')))
            if response.likes_remaining is not None and response.likes_remaining == 0:
                return False
            actions_stub = proto.actions_pb2_grpc.ActionsStub(channel=channel)
            actions_stub.UpdateLiked(LikedStatusRequest(liked=True, user_id=user.id))
            return True

    def fetch_remaining_likes(self) -> RemainingLikesDao:
        url: str = '%s/v2/profile?include=likes' % self.base_url
        request = self.pool_manager.request(method='GET', url=url, headers=self.request_headers)
        if request.status == requests.status_codes.codes.unauthorized:
            raise AuthorizationError(message='while fetching teaser profile')
        return Results.remaining_likes(json_data=json.loads(request.data.decode('utf-8')))

    # def download_images(self, user: UserDao) -> UserDao:
    #     for photo in user.photos:
    #         directory_name: str = 'images/%s' % user.user_id
    #         image_path = '%s/photo_%s.jpg' % (directory_name, math.ceil(random() * 100))
    #         if not os.path.exists(directory_name):
    #             os.mkdir(directory_name)
    #         request = self.pool_manager.request('GET', url=photo.url, preload_content=False)
    #         with open(image_path, 'wb') as out_file:
    #             shutil.copyfileobj(request, out_file)
    #         request.release_conn()
    #         photo.url = image_path
    #     return user

    def process_likes(self) -> None:
        with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
            profiles_stub = proto.profiles_pb2_grpc.ProfilesStub(channel=channel)
            scheduled_profiles: ProfilesReply = profiles_stub.FetchProfilesScheduledForLike(Empty())
            for profile in scheduled_profiles.reply.profiles:
                time.sleep(3)  # sleep for 3 seconds before retrieving and liking
                log_stub = proto.logs_pb2_grpc.LogsStub(channel=channel)
                if self.like_user(user=profile):
                    message: str = 'User %s (%s) is liked!' % (profile.name, profile.user_id)
                    log_stub.LogMessage(
                        LogRequest(message=message, context=self.logging_context, level=LogLevel.INFO.value))
                    actions_stub = proto.actions_pb2_grpc.ActionsStub(channel=channel)
                    actions_stub.UnScheduleLike(ActionsRequest(user_id=profile.id))
                else:
                    log_stub.LogMessage(LogRequest(message='Terminating scheduled likes as no likes are available',
                                                   context=self.logging_context, level=LogLevel.INFO.value))
                    return

    def collect_profiles(self, limit: int = 100) -> None:

        profiles_collected = 0
        new_profiles = 0

        with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
            log_stub = proto.logs_pb2_grpc.LogsStub(channel=channel)
            actions_stub = proto.actions_pb2_grpc.ActionsStub(channel=channel)
            profiles_stub = proto.profiles_pb2_grpc.ProfilesStub(channel=channel)

            while True:
                try:
                    profiles_batch: list[UserDao] = self.get_batch_profile_data()
                except BaseError as e:
                    log_stub.LogMessage(
                        LogRequest(message=e.message, context=self.logging_context, level=LogLevel.INFO.value))
                    return

                batch_size = len(profiles_batch)

                for index in range(0, batch_size):
                    user: UserDao = profiles_batch[index]

                    profiles_collected += 1

                    existing_profile: ProfileIdReply = profiles_stub.FetchProfileByUserId(
                        ProfileUserIdRequest(user_id=user.user_id))
                    if existing_profile.id == 0:
                        actions_stub.AddProfile(AddProfileRequest(
                            bio=user.bio,
                            birth_date=user.birth_date,
                            city=user.city,
                            distance_mi=user.distance,
                            name=user.name,
                            photos=[ProfilePhoto(photo_id=photo.photo_id, url=photo.url) for photo in user.photos],
                            s_number=user.s_number,
                            user_id=user.user_id
                        ))
                        message: str = 'User %s (%s) added to the system' % (user.name, user.user_id)
                        log_stub.LogMessage(
                            LogRequest(message=message, context=self.logging_context, level=LogLevel.INFO.value))
                        new_profiles += 1
                    else:
                        renew_reply: ActionsReply = actions_stub.RenewProfileImages(
                            ActionsPhotoRequest(
                                user_id=existing_profile.id,
                                photos=[ProfilePhoto(
                                    photo_id=photo.photo_id,
                                    url=photo.url
                                ) for photo in user.photos]
                            ))
                        log_stub.LogMessage(LogRequest(message=renew_reply.message, context=self.logging_context,
                                                       level=LogLevel.INFO.value))
                    if profiles_collected >= limit:
                        message: str = 'Terminating collecting profiles, as limit of %s reached, added %s new users' % (
                            limit, new_profiles)
                        log_stub.LogMessage(
                            LogRequest(message=message, context=self.logging_context, level=LogLevel.INFO.value))
                        return

    def collect_teaser(self):
        teaser: Optional[UserTeaserDao] = None
        with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
            try:
                teaser = self.get_teaser_profile()
            except AuthorizationError:
                stub = proto.logs_pb2_grpc.LogsStub(channel=channel)
                stub.LogMessage(
                    LogRequest(message="Authorization error while fetching teaser profile", context="PROCESSOR",
                               level="TRACE"))
            if teaser is not None:
                stub = proto.settings_pb2_grpc.SettingsStub(channel=channel)
                stub.AddTeaser(AddTeaserRequest(teaser=teaser.name))

    def __init__(self):
        with grpc.insecure_channel('%s:%s' % (grpc_host, grpc_port)) as channel:
            stub = proto.settings_pb2_grpc.SettingsStub(channel=channel)
            settings: FetchSettingsReply = stub.FetchSettings(Empty())
            self.base_url = 'https://%s' % settings.base_url
            self.request_headers = {'X-Auth-Token': settings.api_key, 'Host': settings.base_url}
            self.pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
