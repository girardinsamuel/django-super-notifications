# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from super_notifications.app_settings import backends
from super_notifications.models import Notification
from super_notifications.utils import import_callable


def notify_handler(sender, **kwargs):
    recipient = kwargs.pop('recipient', None)

    recipient_list = kwargs.pop('recipient_list', None)

    verb = kwargs.pop('verb', None)
    description = kwargs.pop('description', None)
    nf_type = kwargs.pop('nf_type', 'default')

    actor = kwargs.pop('actor', None)
    actor_text = kwargs.pop('actor_text', None)
    actor_url = kwargs.pop('actor_url', None)

    target = kwargs.pop('target', None)
    target_text = kwargs.pop('target_text', None)
    target_url = kwargs.pop('target_url', None)

    obj = kwargs.pop('obj', None)
    obj_text = kwargs.pop('obj_text', None)
    obj_url = kwargs.pop('obj_url', None)

    level = kwargs.pop('level', 'info')

    extra = kwargs.pop('extra', None)

    if recipient and recipient_list:
        raise TypeError(_("You must specify either a single recipient or a list"
                        " of recipients, not both."))
    elif not recipient and not recipient_list:
        raise TypeError(_("You must specify the recipient of the notification."))

    # if not actor and not actor_text:
    #     raise TypeError(_("Actor not specified."))

    if not verb:
        raise TypeError(_("Verb not specified."))

    if verb:
        if len(verb) > Notification._meta.get_field('verb').max_length:
            raise ValueError(_("Verb is too long."))

    if recipient_list and not isinstance(recipient_list, list):
        raise TypeError(_("Supplied recipient is not an instance of list."))

    if recipient:
        recipient_list = [recipient]

    for user in recipient_list:
        notification = Notification(
            recipient=user,
            verb=verb, description=description, nf_type=nf_type,
            actor_content_object=actor, actor_text=actor_text,
            actor_url_text=actor_url,

            target_content_object=target, target_text=target_text,
            target_url_text=target_url,

            obj_content_object=obj, obj_text=obj_text, obj_url_text=obj_url,
            extra=extra, level=level
        )
        # check that notification can be send
        sent_at_least_once = False
        for backend_id, backend_path in backends:
            backend = import_callable(backend_path)(backend_id)
            if backend.can_send(user, nf_type):
                backend.deliver(user, notification)
                sent_at_least_once = True
        if sent_at_least_once:
            notification.save()