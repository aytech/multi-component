import grpc
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from models.Profiles import User
from protos.actions_pb2 import ActionsRequest, ActionsReply
from protos.actions_pb2_grpc import ActionsServicer
from services.BaseService import BaseService


class Actions(ActionsServicer, BaseService):

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
            return ActionsReply(success=True, message='User %s was hidden' % user.name)
