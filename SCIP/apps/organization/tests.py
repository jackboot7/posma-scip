import pytz
from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.organization.models import Profile, Workday


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="burrg", email="burrg@harrb.gov", password="posma")

    def test_profile_exists(self):
        profile = Profile.objects.get(user=self.user)

        self.assertIsNotNone(profile)

    def test_delete_user(self):
        profile = Profile.objects.get(user=self.user)
        profile_id = profile.id
        self.user.delete()
        profile = Profile.objects.filter(id=profile_id)

        self.assertFalse(profile)


class WorkdayTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="burrg", email="burrg@harrb.gov", password="posma")

    def test_create_workday(self):
        utcnow = datetime.utcnow()
        utcnow = utcnow.replace(tzinfo=pytz.utc)
        work = Workday.objects.create(user=self.user, start=utcnow)

        self.assertIsNotNone(work)

    def test_backward_datetimes(self):
        work = Workday.objects.create(user=self.user,
                                      start=datetime(2013, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC))
        work.finish = datetime(2013, 11, 20, 15, 8, 7, 127325, tzinfo=pytz.UTC)
        # finish time is earlier than start time

        self.assertRaises(ValidationError, work.clean)

    def test_overlapping_datetimes(self):
        work1 = Workday.objects.create(user=self.user,
                                       start=datetime(2013, 11, 20, 9, 8, 7, 127325, tzinfo=pytz.UTC),
                                       finish=datetime(2013, 11, 20, 18, 8, 7, 127325, tzinfo=pytz.UTC))
        work1.save()
        work2 = Workday.objects.create(user=self.user,
                                       start=datetime(2013, 11, 20, 16, 8, 7, 127325, tzinfo=pytz.UTC),
                                       finish=datetime(2013, 11, 20, 23, 8, 7, 127325, tzinfo=pytz.UTC))

        self.assertRaises(ValidationError, work2.clean)

    def test_unclosed_workday(self):
        work1 = Workday.objects.create(user=self.user,
                                       start=datetime(2013, 11, 20, 9, 8, 7, 127325, tzinfo=pytz.UTC))
        work1.save()
        work2 = Workday.objects.create(user=self.user,
                                       start=datetime(2013, 11, 20, 10, 8, 7, 127325, tzinfo=pytz.UTC))

        self.assertRaises(ValidationError, work2.clean)
