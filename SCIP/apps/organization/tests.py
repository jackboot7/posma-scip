import pytz
import factory
#from datetime import datetime
import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.organization.models import Profile, Workday, OrgSettings
from apps.organization import tasks


# =============================================================================
# Model Factories
# =============================================================================


class UserFactory(factory.django.DjangoModelFactory):
    """
    Class for creating User instances for testing purposes
    """
    class Meta:
        model = User

    first_name = "John"
    last_name = "Connor"
    password = "1234"
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    username = factory.Sequence(lambda n: u'johnny%d' % n)
    is_staff = False
    is_superuser = False


class WorkdayFactory(factory.django.DjangoModelFactory):
    """
    Class for creating Workday instances for testing purposes
    """
    class Meta:
        model = Workday

    user = factory.SubFactory(UserFactory)
    start = factory.LazyAttribute(lambda a: datetime.datetime.utcnow().replace(tzinfo=pytz.utc))


class SettingsFactory(factory.django.DjangoModelFactory):
    """
    Class for creating User instances for testing purposes
    """
    class Meta:
        model = OrgSettings

    default_checkout_time = datetime.time(18, 30)
    scheduled_verification_time = datetime.time(20, 0)
    checkout_reminder_time = datetime.time(17, 15)
    checkout_task = None
    reminder_task = None


# =============================================================================
# Organization Models Test cases
# =============================================================================


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
        utcnow = datetime.datetime.utcnow()
        utcnow = utcnow.replace(tzinfo=pytz.utc)
        work = Workday.objects.create(user=self.user, start=utcnow)

        self.assertIsNotNone(work)

    def test_backward_datetimes(self):
        work = Workday.objects.create(user=self.user,
                                      start=datetime.datetime(2013, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC))
        work.finish = datetime.datetime(2013, 11, 20, 15, 8, 7, 127325, tzinfo=pytz.UTC)
        # finish time is earlier than start time

        self.assertRaises(ValidationError, work.clean)

    def test_overlapping_datetimes(self):
        work1 = Workday.objects.create(user=self.user,
                                       start=datetime.datetime(2013, 11, 20, 9, 8, 7, 127325, tzinfo=pytz.UTC),
                                       finish=datetime.datetime(2013, 11, 20, 18, 8, 7, 127325, tzinfo=pytz.UTC))
        work1.save()
        work2 = Workday.objects.create(user=self.user,
                                       start=datetime.datetime(2013, 11, 20, 16, 8, 7, 127325, tzinfo=pytz.UTC),
                                       finish=datetime.datetime(2013, 11, 20, 23, 8, 7, 127325, tzinfo=pytz.UTC))

        self.assertRaises(ValidationError, work2.clean)

    def test_unclosed_workday(self):
        work1 = Workday.objects.create(user=self.user,
                                       start=datetime.datetime(2013, 11, 20, 9, 8, 7, 127325, tzinfo=pytz.UTC))
        work1.save()
        work2 = Workday.objects.create(user=self.user,
                                       start=datetime.datetime(2013, 11, 20, 10, 8, 7, 127325, tzinfo=pytz.UTC))

        self.assertRaises(ValidationError, work2.clean)


class OrgSettingsTestCase(TestCase):
    def setUp(self):
        self.settings = SettingsFactory()

    def test_tasks_created(self):
        self.assertIsNotNone(self.settings.checkout_task)
        self.assertIsNotNone(self.settings.reminder_task)


class CeleryTasksTestCase(TestCase):
    def setUp(self):
        self.settings = SettingsFactory()
        self.users = UserFactory.create_batch(3)
        utcnow = datetime.datetime.utcnow()
        self.now = utcnow.replace(tzinfo=pytz.utc)

    def test_checkout_task(self):
        work1 = WorkdayFactory.create(user=self.users[0])
        work2 = WorkdayFactory.create(user=self.users[1])
        work3 = WorkdayFactory.create(user=self.users[2])

        # workday starting at 9:30am, should be closed automatically
        work1.start = datetime.datetime(year=self.now.year,
                                        month=self.now.month,
                                        day=self.now.day,
                                        hour=9,
                                        minute=30,
                                        second=0,
                                        tzinfo=pytz.UTC)

        # workday starting at 8:30pm. It shouldn't be closed.
        work2.start = datetime.datetime(year=self.now.year,
                                        month=self.now.month,
                                        day=self.now.day,
                                        hour=20,
                                        minute=30,
                                        second=0,
                                        tzinfo=pytz.UTC)

        # workday started "yesterday" at night. It should be closed with today's date.
        yesterday = self.now + datetime.timedelta(days=-1)
        work3.start = datetime.datetime(year=yesterday.year,
                                        month=yesterday.month,
                                        day=yesterday.day,
                                        hour=23,
                                        minute=55,
                                        second=0,
                                        tzinfo=pytz.UTC)

        work1.save()
        work2.save()
        work3.save()

        tasks.automatic_checkout()

        self.assertEqual(Workday.objects.get(id=work1.id).finish.time(), self.settings.default_checkout_time)
        self.assertIsNone(Workday.objects.get(id=work2.id).finish)
        self.assertEqual(Workday.objects.get(id=work3.id).finish.date().day, self.now.day)
