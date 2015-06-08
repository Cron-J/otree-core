#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from otree.models.session import (Participant, Session)


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = [
            '_id_in_session_display',
            'code',
            'label',
            '_pages_completed',
            '_current_app_name',
            '_round_number',
            '_current_page_name',
            'status',
            'last_request_succeeded',
            '_last_page_timestamp',
        ]

class SessionTypeSerializer(serializers.Serializer):
    """docstring for SessionTypeSeriazlizer"""
    name = serializers.CharField(max_length=255)
    display_name = serializers.CharField(max_length=255)
    num_demo_participants = serializers.IntegerField()

class SessionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Session
        lookup_field = 'code'
