# -*- coding: utf-8 -*-
from rest_framework import serializers

from super_notifications.models import Notification


class AbstractNotificationSerializer(serializers.ModelSerializer):

    message = serializers.SerializerMethodField()
    def get_message(self, obj):
        # load templates
        return obj.message


    class Meta:
        model = Notification
        fields = ('id', 'level', 'created', 'read', 'deleted', 'message', 'nf_type')
                  # 'actor_content_object', 'target_content_object', 'obj_content_object')
