# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/actions.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14protos/actions.proto\"!\n\x0e\x41\x63tionsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"T\n\x0c\x41\x63tionsReply\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x15\n\x08s_number\x18\x03 \x01(\x03H\x00\x88\x01\x01\x42\x0b\n\t_s_number2\xa0\x01\n\x07\x41\x63tions\x12\x30\n\x0cScheduleLike\x12\x0f.ActionsRequest\x1a\r.ActionsReply\"\x00\x12\x32\n\x0eUnScheduleLike\x12\x0f.ActionsRequest\x1a\r.ActionsReply\"\x00\x12/\n\x0bHideProfile\x12\x0f.ActionsRequest\x1a\r.ActionsReply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.actions_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ACTIONSREQUEST._serialized_start=24
  _ACTIONSREQUEST._serialized_end=57
  _ACTIONSREPLY._serialized_start=59
  _ACTIONSREPLY._serialized_end=143
  _ACTIONS._serialized_start=146
  _ACTIONS._serialized_end=306
# @@protoc_insertion_point(module_scope)
