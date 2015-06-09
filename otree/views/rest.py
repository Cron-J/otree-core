#!/usr/bin/env python
# encoding: utf-8

from otree.models.session import Session
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from otree.serializers import (ParticipantSerializer, SessionTypeSerializer)
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

class SessionsView(APIView):
    def post(self, request, format=None):
        try:
            response = create_session(session_type_name=self.request.DATA.get('session_type_name'), label=self.request.DATA.get('label'),num_participants=self.request.DATA.get('num_participants'))
            return Response(response.code, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)