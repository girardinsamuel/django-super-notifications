from django import template
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from notify import notify_settings

register = template.Library()


class RenderNotificationsNode(template.Node):

    """
    Template node to parse the token supplied and then generate html
    using the template of corresponding notification.
    """

    @classmethod
    def handle_token(cls, parser, token):
        tokens = token.split_contents()

        if tokens[1] != 'using':
            raise template.TemplateSyntaxError(
                "The second argument in %r must be 'for'" % (tokens[0]))

        if len(tokens) == 3:
            return cls(parser.compile_filter(tokens[2]))
        elif len(tokens) == 5:
            if tokens[3] != 'for':
                raise template.TemplateSyntaxError(
                    "The second argument in %r must be 'for'" % (tokens[0]))
            return cls(obj=parser.compile_filter(tokens[2]), target=tokens[4])
        else:
            raise template.TemplateSyntaxError(
                "%r takes 2 or 3 arguments, %r given." % len(tokens))

    def __init__(self, obj, target='page'):
        self.obj = obj
        self.target = target

    # @staticmethod
    def generate_html(self, notifications):
        """
        Generates rendered HTML content using supplied notifications.
        :param notifications: Notification QuerySet Object
        :return: Rendered HTML.
        """
        html_chunks = []
        template_dir = 'notifications/includes/'
        for notification in notifications:

            template_name = notification.nf_type

            if self.target == 'box':
                suffix = '_box.html'
                nf_ctx = notification.as_json()
            else:
                suffix = '.html'
                nf_ctx = {'notification': notification}

            templates = [
                "{0}{1}{2}".format(template_dir, template_name, suffix),
                "{0}default{1}".format(template_dir, suffix)]

            html = render_to_string(templates, nf_ctx)

            html_chunks.append(html)
        else:
            html_chunks.append("<b>No notifications yet.</b>")
        html_string = '\n'.join(html_chunks)
        return html_string

    def render(self, context):
        """
        Render method of the template tag, returns generated html content to
        the parent template where it was called.
        :param context: Template context.
        :return: Generated HTML content using notification queryset object.
        """
        notifications = self.obj.resolve(context)
        return self.generate_html(notifications)


@register.tag
def render_notifications(parser, token):
    """
    Example::
        {% render_notifications for NOTIFICATION_QUERYSET_OBJECT %}

    :param parser: default arg
    :param token: default arg
    :return: Rendered HTML content for supplied notification QuerySet.
    """
    return RenderNotificationsNode.handle_token(parser, token)


@register.inclusion_tag('notifications/includes/js_variables.html')
def include_notify_js_variables():
    """
    Inclusion template tag to include all JS variables required by the
    notify.js file on the HTML page around <script> tags.

    Example::
        {% include_notify_js_variables %}

    :return: Prepares context for rendering in the inclusion file.
    """
    ctx = {
        'update_notification': reverse('notifications:update'),
        'mark_notification': reverse('notifications:mark'),
        'mark_all_notification': reverse('notifications:mark_all'),
        'delete_notification': reverse('notifications:delete'),

        'nf_list_class_selector': notify_settings.NF_LIST_CLASS_SELECTOR,
        'nf_class_selector': notify_settings.SINGLE_NF_CLASS_SELECTOR,
        'nf_box_list_class_selector': notify_settings.NF_BOX_CLASS_SELECTOR,
        'nf_box_class_selector': notify_settings.SINGLE_NF_BOX_CLASS_SELECTOR,

        'nf_mark_selector': notify_settings.MARK_NF_CLASS_SELECTOR,
        'nf_mark_all_selector': notify_settings.MARK_ALL_NF_CLASS_SELECTOR,
        'nf_delete_selector': notify_settings.DELETE_NF_CLASS_SELECTOR,

        'nf_read_class': notify_settings.READ_NF_CLASS,
        'nf_unread_class': notify_settings.UNREAD_NF_CLASS,

        'nf_update_time_interval': notify_settings.UPDATE_TIME_INTERVAL,
    }
    return ctx