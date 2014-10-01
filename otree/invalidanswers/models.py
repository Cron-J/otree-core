from django.utils.timezone import now
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from otree.db import models


class InvalidAnswer(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.CharField(max_length=100)
    content_object = GenericForeignKey('content_type', 'object_id')

    field_name = models.CharField(max_length=100)
    value = models.TextField(blank=True, null=True)
    error_message = models.TextField()

    player_content_type = models.ForeignKey(ContentType, related_name='+', null=True, blank=True)
    player_object_id = models.CharField(max_length=100, null=True, blank=True)
    player = GenericForeignKey('player_content_type', 'player_object_id')

    created = models.DateTimeField(default=now)

    class Meta:
        app_label = 'otree'

    def __unicode__(self):
        return u'{field}={value}'.format(
            field=self.field_name,
            value=self.value)
