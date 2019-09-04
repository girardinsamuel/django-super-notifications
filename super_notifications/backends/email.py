# -*- coding: utf-8 -*-
from os.path import join

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .dashboard import BaseBackend


class EmailBackend(BaseBackend):
    """
    The email backend sends the notification by email.
    """

    def can_send(self, user, nf_type_label):
        """
        Determines whether this backend is allowed to send a notification to
        the given user and notice_type.
        """
        can_send = super(EmailBackend, self).can_send(user, nf_type_label)
        # check that user has a verified email
        if can_send and user.email:
            return True
        return False

    def deliver(self, recipient, notification):
        """
        Deliver a notification to the given recipients.
        """
        # render notification for this backend
        subject, body = self.render(notification)
        # TODO: use Celery to differ the task
        send_mail(subject, body, settings.FROM_EMAIL, [recipient.email])

    def render(self, notification):
        """Render a notification with the template for this backend."""
        template_body, template_subject = self.get_templates(notification.nf_type)
        subject = render_to_string(template_subject, notification.as_json())
        body = render_to_string(template_body, notification.as_json())
        return subject, body

    def get_templates(self, nf_type_label):
        """
        Returns the notification template to use with this media. This can then be used in the deliver method.
        """
        backend_templates_dir = join(settings.NOTIFICATIONS_TEMPLATES_DIR, self.channel_id)
        template_body = join(backend_templates_dir, "{0}_body.html".format(nf_type_label))
        template_subject = join(backend_templates_dir, "{0}_subject.txt".format(nf_type_label))
        return template_body, template_subject
