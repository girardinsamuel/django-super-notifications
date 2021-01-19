# -*- coding: utf-8 -*-
from rest_framework import routers

from super_notifications.api.views import NotificationsViewSet

notifications_router = routers.SimpleRouter()
notifications_router.register(r'notifications', NotificationsViewSet, basename='notifications-list')
