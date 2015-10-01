#!/usr/bin/env python
# encoding: utf-8

from django.views.generic import View
from django.http import JsonResponse

from otree.models.session import Session
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from otree.serializers import (ParticipantSerializer, SessionTypeSerializer, SessionSerializer)
from otree.session import (create_session, get_session_configs_list)
from django.core import serializers 
import json

def getSerializableObject(obj, isList = False):
    data = serializers.serialize('json', (obj if isList else [obj,]))
    struct = json.loads(data)
    return struct if isList else struct[0]

class Ping(View):

    def get(self, request):
        response = JsonResponse({"ping": True})
        response["Access-Control-Allow-Origin"] = "*"
        return response


class SessionParticipantsList(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        session_code = self.kwargs['session_code']
        return Session.objects.get(code=session_code).get_participants()

class SessionTypesList(generics.ListCreateAPIView):
    serializer_class = SessionTypeSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        return get_session_configs_list()
        # return get_session_types_list()

class SessionsView(APIView):
    def get(self, request, format=None):
        data = self.request.GET
        sessions = getSerializableObject(Session.objects.all(), True) if 'session_code' not in data else getSerializableObject(Session.objects.get(code=data['session_code']))
        return Response(sessions, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:           
            data = self.request.data       
            print(data['session_type_name'])      
            session = create_session(session_config_name=data['session_type_name'], label=data['label'] or '',num_participants=data['num_participants'])
            return Response(session.code, status=status.HTTP_200_OK)
            # return Response(getSerializableObject(session, False), status=status.HTTP_200_OK)#Get entire session object
        except Exception as e:
            return Response(e.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SessionResultsView(APIView):
    def get(self, request, format=None):
        data = self.request.GET
        session = Session.objects.get(code=data['session_code'])
        # results = get_session_results(session)
        return Response(session, status=status.HTTP_200_OK)
