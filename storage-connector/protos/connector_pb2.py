# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/connector.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16protos/connector.proto\"B\n\x0fProfilesRequest\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x11\n\tpage_size\x18\x03 \x01(\x05\"W\n\x15ProfilesSearchRequest\x12\r\n\x05value\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x0c\n\x04page\x18\x03 \x01(\x05\x12\x11\n\tpage_size\x18\x04 \x01(\x05\"\x9c\x03\n\rProfilesReply\x12#\n\x05reply\x18\x01 \x01(\x0b\x32\x14.ProfilesReply.Reply\x1a-\n\x0cProfilePhoto\x12\x10\n\x08photo_id\x18\x02 \x01(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\x1a\xf4\x01\n\x07Profile\x12\x0b\n\x03\x61ge\x18\x01 \x01(\x05\x12\x0b\n\x03\x62io\x18\x02 \x01(\t\x12\x12\n\nbirth_date\x18\x03 \x01(\t\x12\x0c\n\x04\x63ity\x18\x04 \x01(\t\x12\x0f\n\x07\x63reated\x18\x05 \x01(\t\x12\x10\n\x08\x64istance\x18\x06 \x01(\x02\x12\n\n\x02id\x18\x07 \x01(\x05\x12\r\n\x05liked\x18\x08 \x01(\x08\x12\x0c\n\x04name\x18\t \x01(\t\x12+\n\x06photos\x18\n \x03(\x0b\x32\x1b.ProfilesReply.ProfilePhoto\x12\x10\n\x08s_number\x18\x0b \x01(\x03\x12\x11\n\tscheduled\x18\x0c \x01(\x08\x12\x0f\n\x07user_id\x18\r \x01(\t\x1a@\n\x05Reply\x12(\n\x08profiles\x18\x01 \x03(\x0b\x32\x16.ProfilesReply.Profile\x12\r\n\x05total\x18\x02 \x01(\x05\x32|\n\tConnector\x12\x33\n\rFetchProfiles\x12\x10.ProfilesRequest\x1a\x0e.ProfilesReply\"\x00\x12:\n\x0eSearchProfiles\x12\x16.ProfilesSearchRequest\x1a\x0e.ProfilesReply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.connector_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PROFILESREQUEST._serialized_start=26
  _PROFILESREQUEST._serialized_end=92
  _PROFILESSEARCHREQUEST._serialized_start=94
  _PROFILESSEARCHREQUEST._serialized_end=181
  _PROFILESREPLY._serialized_start=184
  _PROFILESREPLY._serialized_end=596
  _PROFILESREPLY_PROFILEPHOTO._serialized_start=238
  _PROFILESREPLY_PROFILEPHOTO._serialized_end=283
  _PROFILESREPLY_PROFILE._serialized_start=286
  _PROFILESREPLY_PROFILE._serialized_end=530
  _PROFILESREPLY_REPLY._serialized_start=532
  _PROFILESREPLY_REPLY._serialized_end=596
  _CONNECTOR._serialized_start=598
  _CONNECTOR._serialized_end=722
# @@protoc_insertion_point(module_scope)
