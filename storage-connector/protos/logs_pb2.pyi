from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogsReply(_message.Message):
    __slots__ = ["logs"]
    class Log(_message.Message):
        __slots__ = ["context", "created", "level", "text"]
        CONTEXT_FIELD_NUMBER: _ClassVar[int]
        CREATED_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        TEXT_FIELD_NUMBER: _ClassVar[int]
        context: str
        created: str
        level: str
        text: str
        def __init__(self, context: _Optional[str] = ..., created: _Optional[str] = ..., level: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[LogsReply.Log]
    def __init__(self, logs: _Optional[_Iterable[_Union[LogsReply.Log, _Mapping]]] = ...) -> None: ...

class LogsRequest(_message.Message):
    __slots__ = ["from_log", "to_log"]
    FROM_LOG_FIELD_NUMBER: _ClassVar[int]
    TO_LOG_FIELD_NUMBER: _ClassVar[int]
    from_log: int
    to_log: int
    def __init__(self, from_log: _Optional[int] = ..., to_log: _Optional[int] = ...) -> None: ...
