import datetime

import grpc
from sqlalchemy import select, update

from models.Profiles import User, Photo
from proto.actions_pb2 import ActionsRequest, ActionsReply, LikedStatusRequest, LikedStatusReply, AddProfileRequest, \
    AddProfileReply, ActionsPhotoRequest
from proto.actions_pb2_grpc import ActionsServicer
from services.BaseService import BaseService


class Actions(ActionsServicer, BaseService):

    def AddProfile(self, request: AddProfileRequest, context: grpc.ServicerContext) -> AddProfileReply:
        creation_date = datetime.datetime.now()
        with self.session as session:
            user: User = User(
                bio=request.bio,
                birth_date=request.birth_date,
                city=request.city,
                created=creation_date,
                distance=0 if request.distance_mi is None else round(request.distance_mi * 1.6, 2),
                liked=False,
                name=request.name,
                photos=[Photo(
                    created=creation_date,
                    photo_id=photo.photo_id,
                    url=photo.url
                ) for photo in request.photos],
                s_number=request.s_number,
                updated=creation_date,
                user_id=request.user_id
            )
            user.age = user.calculate_age()
            session.add(user)
            session.commit()
            print('New user ID: %s' % user.id)
            return AddProfileReply()

    def RenewProfileImages(self, request: ActionsPhotoRequest, context: grpc.ServicerContext) -> ActionsReply:
        user: User = self.session.scalar(statement=select(User).where(User.id == request.user_id))
        if user is not None and user.visible is True:
            with self.session as session:
                for photo in request.photos:
                    session.execute(
                        statement=update(Photo).where(Photo.photo_id == photo.photo_id).values(url=photo.url))
                    session.commit()
                    return ActionsReply(success=True, message='Photo %s updated for user %s (%s)' % (
                        photo.photo_id, user.name, user.s_number))
                user.updated = datetime.datetime.now()
                session.commit()
        return ActionsReply(success=False, message='User %s not found' % request.user_id)

    def ScheduleLike(self, request: ActionsRequest, context: grpc.ServicerContext) -> ActionsReply:
        with self.session as session:
            user: User = session.scalar(statement=select(User).where(User.id == request.user_id))
            if user is None:
                return ActionsReply(success=False, message='User not found')
            if user.liked is False and user.scheduled is False:
                session.execute(statement=update(User).where(User.id == user.id).values(scheduled=True))
                session.commit()
                return ActionsReply(success=True, message='User %s scheduled for like' % user.name)
            else:
                return ActionsReply(success=False, message='User %s is already scheduled or liked' % user.name)

    def UnScheduleLike(self, request: ActionsRequest, context: grpc.ServicerContext) -> ActionsReply:
        with self.session as session:
            user: User = session.scalar(statement=select(User).where(User.id == request.user_id))
            if user is None:
                return ActionsReply(success=False, message='User not found')
            if user.scheduled is True:
                session.execute(statement=update(User).where(User.id == user.id).values(scheduled=False))
                session.commit()
                return ActionsReply(success=True, message='User %s was unscheduled' % user.name)
            else:
                return ActionsReply(success=False, message='User %s is not scheduled' % user.name)

    def HideProfile(self, request: ActionsRequest, context: grpc.ServicerContext) -> ActionsReply:
        with self.session as session:
            user: User = session.scalar(statement=select(User).where(User.id == request.user_id))
            if user is None:
                return ActionsReply(success=False, message='User not found')
            user.visible = False
            session.commit()
            return ActionsReply(success=True, message='User %s was hidden' % user.name, s_number=user.s_number)

    def RestoreProfile(self, request: ActionsRequest, context: grpc.ServicerContext) -> ActionsReply:
        with self.session as session:
            user: User = session.scalar(statement=select(User).where(User.id == request.user_id))
            if user is None:
                return ActionsReply(success=False, message='User not found')
            user.visible = True
            session.commit()
            return ActionsReply(success=True, message='User %s was restored' % user.name, s_number=user.s_number)

    def UpdateLiked(self, request: LikedStatusRequest, context: grpc.ServicerContext) -> LikedStatusReply:
        with self.session as session:
            session.execute(statement=update(User).where(User.id == request.user_id).values(liked=request.liked))
            session.commit()
        return LikedStatusReply(
            success=True
        )
