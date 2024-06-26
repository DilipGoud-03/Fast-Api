# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\x12\x04user\"[\n\x11\x43reateUserRequest\x12\x12\n\nfirst_name\x18\x01 \x01(\t\x12\x11\n\tlast_name\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\"%\n\x12\x43reateUserResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1e\n\x1cListUsersWithContactsRequest\"F\n\x1dListUsersWithContactsResponse\x12%\n\x05users\x18\x01 \x03(\x0b\x32\x16.user.UserWithContacts\")\n\x14UserByContactRequest\x12\x11\n\tparent_id\x18\x01 \x01(\x05\"1\n\x15UserByContactResponse\x12\x18\n\x04user\x18\x01 \x01(\x0b\x32\n.user.User\"u\n\x10UserWithContacts\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x1f\n\x08\x63ontacts\x18\x05 \x03(\x0b\x32\r.user.Contact\"H\n\x04User\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\"I\n\x07\x43ontact\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x11\n\tfirstName\x18\x02 \x01(\t\x12\x10\n\x08lastName\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t2\xf5\x01\n\x0bUserService\x12?\n\nCreateUser\x12\x17.user.CreateUserRequest\x1a\x18.user.CreateUserResponse\x12`\n\x15ListUsersWithContacts\x12\".user.ListUsersWithContactsRequest\x1a#.user.ListUsersWithContactsResponse\x12\x43\n\x08GetUsers\x12\x1a.user.UserByContactRequest\x1a\x1b.user.UserByContactResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CREATEUSERREQUEST']._serialized_start=20
  _globals['_CREATEUSERREQUEST']._serialized_end=111
  _globals['_CREATEUSERRESPONSE']._serialized_start=113
  _globals['_CREATEUSERRESPONSE']._serialized_end=150
  _globals['_LISTUSERSWITHCONTACTSREQUEST']._serialized_start=152
  _globals['_LISTUSERSWITHCONTACTSREQUEST']._serialized_end=182
  _globals['_LISTUSERSWITHCONTACTSRESPONSE']._serialized_start=184
  _globals['_LISTUSERSWITHCONTACTSRESPONSE']._serialized_end=254
  _globals['_USERBYCONTACTREQUEST']._serialized_start=256
  _globals['_USERBYCONTACTREQUEST']._serialized_end=297
  _globals['_USERBYCONTACTRESPONSE']._serialized_start=299
  _globals['_USERBYCONTACTRESPONSE']._serialized_end=348
  _globals['_USERWITHCONTACTS']._serialized_start=350
  _globals['_USERWITHCONTACTS']._serialized_end=467
  _globals['_USER']._serialized_start=469
  _globals['_USER']._serialized_end=541
  _globals['_CONTACT']._serialized_start=543
  _globals['_CONTACT']._serialized_end=616
  _globals['_USERSERVICE']._serialized_start=619
  _globals['_USERSERVICE']._serialized_end=864
# @@protoc_insertion_point(module_scope)
