# -*- coding:utf8 -*-
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
    verification_time = config.scheduled_verification_time
    utcnow = datetime.datetime.utcnow()

    # calculates the date/time the automatic checkout was supposed to happen
    verification_date = utcnow.replace(hour=verification_time.hour,
                                       minute=verification_time.minute,
                                       second=verification_time.second,
                                       tzinfo=pytz.utc)

    # get all unfinished workdays started before the automatic checkout date/time
    workdays = Workday.objects.filter(finish__isnull=True).filter(start__lt=verification_date)

    for wd in workdays:
        work_day = wd.start.date()
        # Cada workday se cierra con fecha del mismo día de iniciarse la jornada.
        # Si la hora de cierre por defecto es más temprana que la hora de inicio, se le suma un día.
        if default < wd.start.time():
            work_day = work_day + datetime.timedelta(days=1)

        wd.finish = datetime.datetime(work_day.year,
                                      work_day.month,
                                      work_day.day,
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
