#!/usr/bin/env python
# encoding: utf-8

from otree.models.session import Session
from rest_framework import generics, permissions
from otree.serializers import (ParticipantSerializer, SessionTypeSerializer, SessionSerializer)
from otree.session import (
    create_session, get_session_types_list
)

class SessionParticipantsList(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        session_code = self.kwargs['session_code']
        return Session.objects.get(code=session_code).get_participants()

class SessionTypesList(generics.ListCreateAPIView):
    serializer_class = SessionTypeSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        return get_session_types_list()

    def perform_create(self, serializer):
        create_session(session_type_name=self.request.DATA.get('name'), num_participants=self.request.DATA.get('num_demo_participants'))

class SessionList(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        session_code = self.kwargs['code']
        return Session.objects.filter(code=session_code)

# class SessionList(generics.RetrieveAPIView):
#     serializer_class = SessionSerializer
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     # queryset = Session.objects.all()
#     def get_queryset(self):
#         #session_code = self.kwargs['session_code']
#         session_code = self.kwargs['code']
#         # return Session.objects.get(code=session_code)
#         return Session.objects.get(code=session_code)

#     def perform_create(self, serializer):
#         session_code = self.kwargs['session_type_name']
#         create_session(session_type_name=self.request.session_type_name, num_participants=self.request.num_participants)

# class SessionList(generics.ListCreateAPIView):
#     serializer_class = SessionSerializer
#     permission_classes = [
#         permissions.AllowAny
#     ]

#     def get_queryset(self):
#         session_code = self.kwargs['code']
#         return Session.objects.filter(code=session_code)

#     def perform_create(self, serializer):
#         create_session(session_type_name=self.request.data.session_type_name, num_participants=self.request.data.num_participants)
