from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

from django.db import models
from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

from os import environ as env

from django.conf import settings
from django.template import Context, Template

line_template = """
Service {{ service.name }} {% if service.overall_status == service.PASSING_STATUS %}*is back to normal*{% else %}reporting *{{ service.overall_status }}* status{% endif %}: {{ scheme }}://{{ host }}{% url 'service' pk=service.id %} \
{% if alert %}{% for alias in users %} @{{ alias }}{% endfor %}{% endif %}\

{% if service.overall_status != service.PASSING_STATUS %}Checks failing:\
{% for check in service.all_failing_checks %}\
    {% if check.check_category == 'Jenkins check' %}\
        {% if check.last_result.error %}\
            - {{ check.name }} ({{ check.last_result.error|safe }}) {{check.jenkins_config.jenkins_api}}job/{{ check.name }}/{{ check.last_result.job_number }}/console
        {% else %}\
            - {{ check.name }} {{check.jenkins_config.jenkins_api}}/job/{{ check.name }}/{{check.last_result.job_number}}/console
        {% endif %}\
    {% else %}
        - {{ check.name }} {% if check.last_result.error %} ({{ check.last_result.error|safe }}){% endif %}
    {% endif %}\
{% endfor %}\
{% endif %}\
"""

# This provides the slack alias for each user. Each object corresponds to a User
class LineAlert(AlertPlugin):
    name = "Line"
    author = "BabyThor@COL"

    def send_alert(self, service, users, duty_officers):
        print 'xxxxxx'
        alert = True
        line_aliases = []
        users = list(users) + list(duty_officers)

        line_aliases = [u.line_alias for u in LineAlertUserData.objects.filter(user__user__in=users)]

        if service.overall_status == service.WARNING_STATUS:
            alert = False  # Don't alert at all for WARNING
        if service.overall_status == service.ERROR_STATUS:
            if service.old_overall_status in (service.ERROR_STATUS, service.ERROR_STATUS):
                alert = False  # Don't alert repeatedly for ERROR
        if service.overall_status == service.PASSING_STATUS:
            color = 'good'
            if service.old_overall_status == service.WARNING_STATUS:
                alert = False  # Don't alert for recovery from WARNING status
        else:
            color = 'danger'

        c = Context({
            'service': service,
            'users': line_aliases,
            'host': settings.WWW_HTTP_HOST,
            'scheme': settings.WWW_SCHEME,
            'alert': alert,
        })
        message = Template(line_template).render(c)
        self._send_line_alert(message, service, color=color, sender='Cabot')

    def _send_line_alert(self, message, service, color='good', sender='Cabot'):
        token = env.get('LINE_CHANNEL_ACCESS_TOKEN')
        channel = env.get('LINE_CHANNEL_ID')

        line_bot_api = LineBotApi(token)

        try:
            line_bot_api.push_message(channel, TextSendMessage(text=message))
        except LineBotApiError as e:
            pass

class LineAlertUserData(AlertPluginUserData):
    name = "Line Plugin"
    line_alias = models.CharField(max_length=50, blank=True)

