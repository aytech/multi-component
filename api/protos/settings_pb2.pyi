from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class FetchSettingsReply(_message.Message):
    __slots__ = ["api_key", "base_url", "scheduled", "teasers"]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    BASE_URL_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_FIELD_NUMBER: _ClassVar[int]
    TEASERS_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    base_url: str
    scheduled: int
    teasers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, api_key: _Optional[str] = ..., base_url: _Optional[str] = ..., scheduled: _Optional[int] = ..., teasers: _Optional[_Iterable[str]] = ...) -> None: ...

class FetchSettingsValueReply(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class SettingsReply(_message.Message):
    __slots__ = ["message", "success"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    message: str
    success: bool
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class SettingsRequest(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...
