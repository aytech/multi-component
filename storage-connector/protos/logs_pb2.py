# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/logs.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11protos/logs.proto\"Q\n\x0bLogsRequest\x12\x15\n\x08\x66rom_log\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x13\n\x06to_log\x18\x02 \x01(\x05H\x01\x88\x01\x01\x42\x0b\n\t_from_logB\t\n\x07_to_log\"o\n\tLogsReply\x12\x1c\n\x04logs\x18\x01 \x03(\x0b\x32\x0e.LogsReply.Log\x1a\x44\n\x03Log\x12\x0f\n\x07\x63ontext\x18\x01 \x01(\t\x12\x0f\n\x07\x63reated\x18\x02 \x01(\t\x12\r\n\x05level\x18\x03 \x01(\t\x12\x0c\n\x04text\x18\x04 \x01(\t2/\n\x04Logs\x12\'\n\tFetchLogs\x12\x0c.LogsRequest\x1a\n.LogsReply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.logs_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LOGSREQUEST._serialized_start=21
  _LOGSREQUEST._serialized_end=102
  _LOGSREPLY._serialized_start=104
  _LOGSREPLY._serialized_end=215
  _LOGSREPLY_LOG._serialized_start=147
  _LOGSREPLY_LOG._serialized_end=215
  _LOGS._serialized_start=217
  _LOGS._serialized_end=264
# @@protoc_insertion_point(module_scope)
