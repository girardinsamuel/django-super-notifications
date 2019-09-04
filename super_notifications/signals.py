from django.dispatch import Signal

from super_notifications.handler import notify_handler

notify = Signal(providing_args=[
    'recipient', 'recipient_list',
    'actor', 'actor_text', 'actor_url',
    'verb', 'description', 'nf_type',
    'target', 'target_text', 'target_url',
    'obj', 'obj_text', 'obj_url',
    'extra', 'level'
])

notify.connect(notify_handler, sender=None, dispatch_uid='super_notifications.notify')
