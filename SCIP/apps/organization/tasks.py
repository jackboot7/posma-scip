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
    and it was started before the default checkout time.
    """
    config = OrgSettings.objects.first()   # Later on, it should filter by organization
    default = config.default_checkout_time
    utcnow = datetime.datetime.utcnow()
    checkout_time = utcnow.replace(hour=default.hour, minute=default.minute, second=default.second, tzinfo=pytz.utc)

    workdays = Workday.objects.filter(finish__isnull=True).filter(start__lt=checkout_time)

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
        send_mail('[Posma Group] Cierre de jornada en SCIP',
                  '%s, recuerda marcar el cierre de tu jornada laboral al terminar.\n\n http://scip.posmagroup.com/ \n\n Gracias!' % user.first_name,
                  settings.EMAIL_FROM_USER,
                  [user.email],
                  fail_silently=False)
