import pytz
import datetime

from django.core.mail import send_mail
from django.conf import settings

from SCIP.celery import app
from apps.organization.models import Workday, OrgSettings


@app.task
def automatic_checkout():
    """
    Automatically closes all pending workdays if finish datetime is not set
    """
    workdays = Workday.objects.filter(finish__isnull=True)
    config = OrgSettings.objects.first()   # Later on, it should filter by organization
    default = config.default_checkout_time
    today = datetime.date.today()

    for wd in workdays:
        wd.finish = datetime.datetime(today.year,
                                      today.month,
                                      today.day,
                                      default.hour,
                                      default.minute,
                                      default.second,
                                      tzinfo=pytz.UTC)
        wd.save()


@app.task
def checkout_notification():
    workdays = Workday.objects.filter(finish__isnull=True)
    users = [wd.user for wd in workdays]

    for user in users:
        send_mail('Cierre de jornada',
                  '%s, recuerda marcar el cierre de tu jornada laboral al terminar. Gracias!' % user.first_name,
                  settings.EMAIL_FROM_USER,
                  [user.email],
                  fail_silently=False)
