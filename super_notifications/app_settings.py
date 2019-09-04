# -*- coding: utf-8 -*-

from django.conf import settings

from super_notifications.api.serializers import AbstractNotificationSerializer as DefaultNotificationSerializer
from .utils import import_callable

NotificationSerializer = import_callable(
    getattr(settings, 'NOTIFICATIONS_SERIALIZER', DefaultNotificationSerializer))

backends = getattr(settings, 'NOTIFICATIONS_BACKENDS',
                   [("dashboard", "super_notifications.backends.dashboard.BaseBackend")])
