from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ActionsReply(_message.Message):
    __slots__ = ["message", "s_number", "success"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    S_NUMBER_FIELD_NUMBER: _ClassVar[int]
    message: str
    s_number: int
    success: bool
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., s_number: _Optional[int] = ...) -> None: ...

class ActionsRequest(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...
