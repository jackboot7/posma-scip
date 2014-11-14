import pytz
from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.organization.models import *


class WorkdayTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="burrg", email="burrg@harrb.gov", password="posma")
        self.employee = Employee.objects.create(user=user)

    def test_create_workday(self):
        utcnow = datetime.utcnow()
        utcnow = utcnow.replace(tzinfo=pytz.utc)
        work = Workday.objects.create(employee=self.employee, start=utcnow)
        self.assertIsNotNone(work)

    def test_backward_datetimes(self):
        work = Workday.objects.create(employee=self.employee,
                                      start=datetime(2013, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC))
        work.finish = datetime(2013, 11, 20, 15, 8, 7, 127325, tzinfo=pytz.UTC)
        # finish time is earlier than start time
        self.assertRaises(ValidationError, work.clean)

    def test_overlapping_datetimes(self):
        work1 = Workday.objects.create(employee=self.employee,
                                       start=datetime(2013, 11, 20, 9, 8, 7, 127325, tzinfo=pytz.UTC),
                                       finish=datetime(2013, 11, 20, 18, 8, 7, 127325, tzinfo=pytz.UTC))
        work1.save()
        work2 = Workday.objects.create(employee=self.employee,
                                       start=datetime(2013, 11, 20, 16, 8, 7, 127325, tzinfo=pytz.UTC),
                                       finish=datetime(2013, 11, 20, 23, 8, 7, 127325, tzinfo=pytz.UTC))

        self.assertRaises(ValidationError, work2.clean)
