# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/settings.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15protos/settings.proto\" \n\x0fSettingsRequest\x12\r\n\x05value\x18\x01 \x01(\t\"1\n\rSettingsReply\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"[\n\x12\x46\x65tchSettingsReply\x12\x0f\n\x07\x61pi_key\x18\x01 \x01(\t\x12\x10\n\x08\x62\x61se_url\x18\x02 \x01(\t\x12\x11\n\tscheduled\x18\x03 \x01(\x05\x12\x0f\n\x07teasers\x18\x04 \x03(\t\"(\n\x17\x46\x65tchSettingsValueReply\x12\r\n\x05value\x18\x01 \x01(\t\"\x07\n\x05\x45mpty2\x90\x02\n\x08Settings\x12\x35\n\x0f\x41\x64\x64UpdateApiKey\x12\x10.SettingsRequest\x1a\x0e.SettingsReply\"\x00\x12\x36\n\x10\x41\x64\x64UpdateBaseUrl\x12\x10.SettingsRequest\x1a\x0e.SettingsReply\"\x00\x12\x31\n\x0b\x46\x65tchApiKey\x12\x06.Empty\x1a\x18.FetchSettingsValueReply\"\x00\x12\x32\n\x0c\x46\x65tchBaseUrl\x12\x06.Empty\x1a\x18.FetchSettingsValueReply\"\x00\x12.\n\rFetchSettings\x12\x06.Empty\x1a\x13.FetchSettingsReply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.settings_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SETTINGSREQUEST._serialized_start=25
  _SETTINGSREQUEST._serialized_end=57
  _SETTINGSREPLY._serialized_start=59
  _SETTINGSREPLY._serialized_end=108
  _FETCHSETTINGSREPLY._serialized_start=110
  _FETCHSETTINGSREPLY._serialized_end=201
  _FETCHSETTINGSVALUEREPLY._serialized_start=203
  _FETCHSETTINGSVALUEREPLY._serialized_end=243
  _EMPTY._serialized_start=245
  _EMPTY._serialized_end=252
  _SETTINGS._serialized_start=255
  _SETTINGS._serialized_end=527
# @@protoc_insertion_point(module_scope)
