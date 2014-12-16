import pytz
import datetime

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
