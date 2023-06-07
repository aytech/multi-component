import sys

import grpc
from sqlalchemy import Select, select, func
from sqlalchemy.orm import Session, Query

from enums.LogContext import LogContext
from enums.Status import Status
from models.Profiles import User
from proto.profiles_pb2 import ProfilesReply, ProfilesRequest, ProfilesSearchRequest
from proto.profiles_pb2_grpc import ProfilesServicer
from services.BaseService import BaseService

sys.path.append('..')


class Profiles(ProfilesServicer, BaseService):

    @staticmethod
    def get_profile(user: User) -> ProfilesReply.Profile:
        return ProfilesReply.Profile(
            age=user.get_age(),
            bio=user.bio,
            birth_date=user.birth_date,
            city=user.city,
            created=user.get_created(),
            distance=0 if user.distance_mi is None else round(user.distance_mi * 1.6, 2),
            id=user.id,
            liked=user.liked,
            name=user.name,
            photos=[ProfilesReply.ProfilePhoto(
                photo_id=photo.photo_id,
                url=photo.url
            ) for photo in user.photos],
            s_number=user.s_number,
            scheduled=user.scheduled,
            user_id=user.user_id
        )

    def fetch_all_users_count(self, status: str):
        query: Query = self.session.query(func.count(User.id))
        if status == Status.liked:
            query = query.filter(User.visible, User.liked)
        elif status == Status.scheduled:
            query = query.filter(User.visible, User.scheduled)
        elif status == Status.new:
            query = query.filter(User.visible, User.scheduled.is_(False), User.liked.is_(False))
        else:
            query = query.filter(User.visible)
        return query.scalar()

    def fetch_filtered_users_count(self, name_partial: str, status: str):
        query: Query = self.session.query(func.count(User.id))
        if status == Status.liked:
            query = query.filter(User.visible, User.liked)
        elif status == Status.scheduled:
            query = query.filter(User.visible, User.scheduled)
        elif status == Status.new:
            query = query.filter(User.visible, User.scheduled.is_(False), User.liked.is_(False))
        else:
            query = query.filter(User.visible)
        return query.where(User.name.ilike('%{}%'.format(name_partial))).scalar()

    def FetchProfiles(self, request: ProfilesRequest, context: grpc.ServicerContext) -> ProfilesReply:
        statement: Select = select(User).filter(User.visible)
        if request.status == Status.liked:
            statement = statement.filter(User.liked)
        elif request.status == Status.scheduled:
            statement = statement.filter(User.scheduled)
        elif request.status == Status.new:
            statement = statement.filter(User.liked.is_(False), User.scheduled.is_(False))
        # paginate
        statement = statement.order_by(User.created.desc()).offset((request.page - 1) * request.page_size).limit(
            request.page_size)
        self.log_message(message=str(statement), context=LogContext.SQL)
        return ProfilesReply(
            reply=ProfilesReply.Reply(
                profiles=[self.get_profile(user=user) for user in self.session.scalars(statement=statement).all()],
                total=self.fetch_all_users_count(request.status)
            )
        )

    def SearchProfiles(self, request: ProfilesSearchRequest, context: grpc.ServicerContext) -> ProfilesReply:
        self.log_message(
            message='Parameters received: value: %s, status: %s, page: %s, page_size: %s' % (
                request.value, request.status, request.page, request.page_size),
            context='%s:SearchProfiles' % LogContext.SQL)
        statement: Select = select(User).where(User.name.ilike('%{}%'.format(request.value)))
        if request.status == Status.liked:
            statement = statement.filter(User.visible, User.liked)
        elif request.status == Status.scheduled:
            statement = statement.filter(User.visible, User.scheduled)
        elif request.status == Status.new:
            statement = statement.filter(User.visible, User.scheduled.is_(False), User.liked.is_(False))
        else:
            statement = statement.filter(User.visible)
        statement = statement.order_by(User.created.desc()).offset((request.page - 1) * request.page_size).limit(
            request.page_size)
        self.log_message(message=str(statement), context=LogContext.SQL)
        return ProfilesReply(
            reply=ProfilesReply.Reply(
                profiles=[self.get_profile(user=user) for user in self.session.scalars(statement=statement).all()],
                total=self.fetch_filtered_users_count(request.value, request.status)
            )
        )
