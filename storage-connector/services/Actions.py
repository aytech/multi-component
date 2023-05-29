import grpc
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from models.Profiles import User
from protos.actions_pb2 import LikeRequest, LikeReply
from protos.actions_pb2_grpc import ActionsServicer


class Actions(ActionsServicer):
    session: Session

    def ScheduleLike(self, request: LikeRequest, context: grpc.ServicerContext) -> LikeReply:
        with self.session as session:
            user: User = session.scalar(statement=select(User).where(User.id == request.user_id))
            if user is None:
                return LikeReply(success=False, message='User not found')
            if user.liked is False and user.scheduled is False:
                session.execute(statement=update(User).where(User.id == user.id).values(scheduled=True))
                session.commit()
                return LikeReply(success=True, message='User %s scheduled for like' % user.name)
            else:
                return LikeReply(success=False, message='User %s is already scheduled or liked' % user.name)

    def UnScheduleLike(self, request: LikeRequest, context: grpc.ServicerContext) -> LikeReply:
        with self.session as session:
            user: User = session.scalar(statement=select(User).where(User.id == request.user_id))
            if user is None:
                return LikeReply(success=False, message='User not found')
            if user.scheduled is True:
                session.execute(statement=update(User).where(User.id == user.id).values(scheduled=False))
                session.commit()
                return LikeReply(success=True, message='User %s was unscheduled' % user.name)
            else:
                return LikeReply(success=False, message='User %s is not scheduled' % user.name)

    def __init__(self, session: Session):
        self.session = session
