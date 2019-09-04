# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist


class BaseBackend(object):
    """
    The base backend which does not send the notification somewhere.
    """
    def __init__(self, channel_id):
        self.channel_id = channel_id

    def can_send(self, user, nf_type_label):
        """
        Determines whether this backend is allowed to send a notification to
        the given user and notice_type.
        """
        try:
            user.notifications_settings.get(notification_type__label=nf_type_label, disabled=False,
                                            channels__contains=self.channel_id)
            return True
        except ObjectDoesNotExist:
            return False

    def deliver(self, recipient, notification):
        """
        Deliver a notification to the given recipients.
        """
        # raise NotImplementedError()
        pass

    def render(self, notification):
        """Render a notification with the template for this backend."""
        raise NotImplementedError()

    def get_templates(self, nf_type_label):
        """
        Returns the notification template to use with this media. This can then be used in the deliver method.
        """
        raise NotImplementedError()
