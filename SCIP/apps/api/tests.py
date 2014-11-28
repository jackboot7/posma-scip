import json
import factory
from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from rest_framework import status
from jsonschema import validate

from apps.api.serializers import *
from apps.api.views import *


def validate_json_schema(schema_name, data):
    schema_file = open("apps/api/schemas/%s.json" % schema_name).read()
    json_data = JSONRenderer().render(data)
    validate(json.loads(json_data), json.loads(schema_file))


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
    start = factory.LazyAttribute(lambda a: datetime.utcnow().replace(tzinfo=pytz.utc))

#=============================================================================
# Serializers Test Cases
#=============================================================================


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.users = UserFactory.build_batch(3)

    def test_users_schema(self):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        try:
            validate_json_schema("users", serializer.data)
        except ValidationError, exc:
            self.fail(exc)

    def test_user_schema(self):
        serializer = UserSerializer(self.users[0])
        try:
            validate_json_schema("user", serializer.data)
        except ValidationError, exc:
            self.fail(exc)


class WorkdaySerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

        self.work1 = WorkdayFactory(user=self.user1)
        self.work2 = WorkdayFactory(user=self.user2)

    def test_workday_schema(self):
        serializer = WorkdaySerializer(self.work1)
        try:
            validate_json_schema("workday", serializer.data)
            # update finish time and validate again
            self.work1.finish = self.work1.start + timedelta(hours=9)
            serializer = WorkdaySerializer(self.work1)
            validate_json_schema("workday", serializer.data)
        except ValidationError, exc:
            self.fail(exc)

    def test_workdays_schema(self):
        workdays = Workday.objects.all()
        serializer = WorkdaySerializer(workdays, many=True)
        try:
            validate_json_schema("workdays", serializer.data)
        except ValidationError, exc:
            self.fail(exc)

#=============================================================================
# API Views Test Cases
#=============================================================================


class EndpointsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(username="admin", password="posma123", email="a@b.com")
        # login using JWT
        """
        response = self.client.post(reverse('login'),
                                    {"username": "dummy", "password": "posma123"},
                                    format="json")
        self.token = response.data['token']
        """
        self.client.login(username='admin', password="posma123")

    def test_user_list(self):
        # GET method
        UserFactory.create_batch(4)
        url = reverse('user_list')
        response = self.client.get(url)
        validate_json_schema("users", response.data)
        self.assertEqual(len(response.data), 4)

        # POST method
        self.client.post(url, {"username": "jackboot7",
                               "first_name": "Luis",
                               "last_name": "Santana",
                               "email": "luis.santana@gmail.com"})
        response = self.client.get(url)
        self.assertEqual(len(response.data), 5)

    def test_user_detail(self):
        # GET method
        UserFactory(username="ospa", first_name="Oscar")
        url = reverse('user_detail', kwargs={'username': "ospa"})
        response = self.client.get(url)
        validate_json_schema("user", response.data)
        self.assertEqual(response.data['first_name'], "Oscar")

        # PUT method
        response = self.client.put(url, {'username': "ospa", 'first_name': "Bob"})
        self.assertEqual(response.data['first_name'], "Bob")

    def test_user_workday_list(self):
        # POST method
        UserFactory.create(username="jackboot7")
        url = reverse('user_workday_list', kwargs={'username': "jackboot7"})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Invalid workday creation
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

        # GET method
        response = self.client.get(url)
        validate_json_schema("workdays", response.data)

    def test_user_last_workday(self):
        # GET method
        user = UserFactory(username="cbruguera")
        WorkdayFactory.create(user=user)
        url = reverse('user_last_workday', kwargs={'username': "cbruguera"})
        response = self.client.get(url)
        validate_json_schema("workday", response.data)

        # PUT method
        response = self.client.put(url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['finish'], datetime)

        # Invalid workday editing
        response = self.client.put(url, {})
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_workday_list(self):
        # POST method
        UserFactory.create(username="cbruguera")
        url = reverse('workday_list')
        response = self.client.post(url, {'user': "cbruguera"})

        # Invalid workday creation
        response = self.client.post(url, {'user': "cbruguera"})
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

        # GET method
        response = self.client.get(url)
        validate_json_schema("workdays", response.data)

    def test_workday_detail(self):
        # GET method
        user = UserFactory.create(username="cbruguera")
        wd = WorkdayFactory(user=user)
        url = reverse('workday_detail', kwargs={'pk': wd.id})
        response = self.client.get(url)
        validate_json_schema("workday", response.data)

        # PUT method
        response = self.client.put(url, {'user': "cbruguera"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Invalid editing
        response = self.client.put(url, {'user': "cbruguera"})
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)
