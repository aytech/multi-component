import datetime
import json

import grpc
from sqlalchemy import Select, select, func

from models.Profiles import User
from proto.empty_pb2 import Empty
from proto.settings_pb2_grpc import SettingsServicer
from proto.settings_pb2 import SettingsRequest, SettingsReply, FetchSettingsReply, FetchSettingsValueReply, \
    TeaserRequest
from services.BaseService import BaseService

from models.Settings import Settings as SettingsModel


class Settings(SettingsServicer, BaseService):

    def get_api_key(self) -> SettingsModel:
        statement: Select = select(SettingsModel).where(SettingsModel.name == SettingsModel.api_key_setting)
        return self.session.scalar(statement=statement)

    def get_base_url(self) -> SettingsModel:
        statement: Select = select(SettingsModel).where(SettingsModel.name == SettingsModel.base_url_setting)
        return self.session.scalar(statement=statement)

    def get_scheduled(self) -> int:
        return self.session.query(func.count(User.id)).filter(User.scheduled).scalar()

    def get_teasers(self) -> list[str]:
        statement: Select = select(SettingsModel).where(SettingsModel.name == SettingsModel.teasers_setting)
        settings: SettingsModel = self.session.scalar(statement=statement)
        if settings is None:
            return []
        return json.loads(settings.value)

    def AddTeaser(self, request: TeaserRequest, context: grpc.ServicerContext) -> Empty:
        statement: Select = select(SettingsModel).where(SettingsModel.name == SettingsModel.teasers_setting)
        teaser_setting: SettingsModel = self.session.scalar(statement=statement)
        teasers: list[str] = []
        if teaser_setting is None:
            teaser_setting = SettingsModel(
                created=datetime.datetime.now(),
                name=SettingsModel.teasers_setting,
            )
        else:
            teasers = json.loads(teaser_setting.value)
        if request.teaser not in teasers:
            teasers.append(request.teaser)
            teaser_setting.value = json.dumps(teasers)
            with self.session as session:
                session.add(teaser_setting)
                session.commit()
        return Empty()

    def AddUpdateApiKey(self, request: SettingsRequest, context: grpc.ServicerContext) -> SettingsReply:
        key: SettingsModel = self.get_api_key()
        if key is None:
            key = SettingsModel(
                created=datetime.datetime.now(),
                name=SettingsModel.api_key_setting,
            )
        key.value = request.value
        with self.session as session:
            session.add(key)
            session.commit()
        return SettingsReply(success=True)

    def AddUpdateBaseUrl(self, request: SettingsRequest, context: grpc.ServicerContext) -> SettingsReply:
        url: SettingsModel = self.get_base_url()
        if url is None:
            url = SettingsModel(
                created=datetime.datetime.now(),
                name=SettingsModel.base_url_setting,
            )
        url.value = request.value
        with self.session as session:
            session.add(url)
            session.commit()
        return SettingsReply(success=True)

    def FetchSettings(self, request: Empty, context: grpc.ServicerContext) -> FetchSettingsReply:
        return FetchSettingsReply(
            api_key=self.get_api_key().value,
            base_url=self.get_base_url().value,
            scheduled=self.get_scheduled(),
            teasers=self.get_teasers()
        )

    def FetchApiKey(self, request: Empty, context: grpc.ServicerContext) -> FetchSettingsValueReply:
        return FetchSettingsValueReply(value=self.get_api_key().value)

    def FetchBaseUrl(self, request: Empty, context: grpc.ServicerContext) -> FetchSettingsValueReply:
        return FetchSettingsValueReply(value=self.get_base_url().value)

    def RemoveTeaser(self, request: TeaserRequest, context: grpc.ServicerContext) -> SettingsReply:
        statement: Select = select(SettingsModel).where(SettingsModel.name == SettingsModel.teasers_setting)
        teaser_setting: SettingsModel = self.session.scalar(statement=statement)
        teasers: list = json.loads(teaser_setting.value)
        filtered_teasers: list = list(filter(lambda teaser: teaser != request.teaser, teasers))
        if filtered_teasers != teasers:  # remove only if found
            teaser_setting.value = json.dumps(filtered_teasers)
            with self.session as session:
                session.add(teaser_setting)
                session.commit()
            return SettingsReply(success=True, message='Teaser %s was removed' % request.teaser)
        else:
            return SettingsReply(success=False, message='Teaser %s not found' % request.teaser)
