from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProfilesReply(_message.Message):
    __slots__ = ["reply"]
    class Profile(_message.Message):
        __slots__ = ["age", "bio", "birth_date", "city", "created", "distance", "id", "liked", "name", "photos", "s_number", "scheduled", "user_id"]
        AGE_FIELD_NUMBER: _ClassVar[int]
        BIO_FIELD_NUMBER: _ClassVar[int]
        BIRTH_DATE_FIELD_NUMBER: _ClassVar[int]
        CITY_FIELD_NUMBER: _ClassVar[int]
        CREATED_FIELD_NUMBER: _ClassVar[int]
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        LIKED_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        PHOTOS_FIELD_NUMBER: _ClassVar[int]
        SCHEDULED_FIELD_NUMBER: _ClassVar[int]
        S_NUMBER_FIELD_NUMBER: _ClassVar[int]
        USER_ID_FIELD_NUMBER: _ClassVar[int]
        age: int
        bio: str
        birth_date: str
        city: str
        created: str
        distance: float
        id: int
        liked: bool
        name: str
        photos: _containers.RepeatedCompositeFieldContainer[ProfilesReply.ProfilePhoto]
        s_number: int
        scheduled: bool
        user_id: str
        def __init__(self, age: _Optional[int] = ..., bio: _Optional[str] = ..., birth_date: _Optional[str] = ..., city: _Optional[str] = ..., created: _Optional[str] = ..., distance: _Optional[float] = ..., id: _Optional[int] = ..., liked: bool = ..., name: _Optional[str] = ..., photos: _Optional[_Iterable[_Union[ProfilesReply.ProfilePhoto, _Mapping]]] = ..., s_number: _Optional[int] = ..., scheduled: bool = ..., user_id: _Optional[str] = ...) -> None: ...
    class ProfilePhoto(_message.Message):
        __slots__ = ["photo_id", "url"]
        PHOTO_ID_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        photo_id: str
        url: str
        def __init__(self, photo_id: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...
    class Reply(_message.Message):
        __slots__ = ["profiles", "total"]
        PROFILES_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        profiles: _containers.RepeatedCompositeFieldContainer[ProfilesReply.Profile]
        total: int
        def __init__(self, profiles: _Optional[_Iterable[_Union[ProfilesReply.Profile, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...
    REPLY_FIELD_NUMBER: _ClassVar[int]
    reply: ProfilesReply.Reply
    def __init__(self, reply: _Optional[_Union[ProfilesReply.Reply, _Mapping]] = ...) -> None: ...

class ProfilesRequest(_message.Message):
    __slots__ = ["page", "page_size", "status"]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    status: str
    def __init__(self, status: _Optional[str] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class ProfilesSearchRequest(_message.Message):
    __slots__ = ["page", "page_size", "status", "value"]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    status: str
    value: str
    def __init__(self, value: _Optional[str] = ..., status: _Optional[str] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...
