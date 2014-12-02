import json
import factory
from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from rest_framework_jwt import utils
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from rest_framework import status
from jsonschema import validate

from apps.api.serializers import *
from apps.api.views import *


def validate_json_schema(schema_name, data):
    """
    Validates JSON data for a given schema, defined as a .json file in the "schemas" folder
    """
    schema_file = open("apps/api/schemas/%s.json" % schema_name).read()
    json_data = JSONRenderer().render(data)
    validate(json.loads(json_data), json.loads(schema_file))    # Raises ValidationError
    return True


#=============================================================================
# Model Factories
#=============================================================================


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
        self.users = UserFactory.create_batch(3)

    def test_user_serialization(self):
        users = User.objects.all()

        # Single object serialization
        serializer = UserSerializer(users[0])
        self.assertEqual(type(serializer), UserSerializer)
        self.assertTrue(validate_json_schema("user", serializer.data))

        # Muliple objects serialization
        serializer = UserSerializer(users, many=True)
        self.assertEqual(type(serializer), UserSerializer)
        self.assertTrue(validate_json_schema("users", serializer.data))

    def test_user_deserialization(self):
        serializer = UserSerializer(data={'username': "ospa",
                                          'password': "holis123",
                                          'first_name': "Oscar",
                                          'last_name': "Paredes"})

        self.assertTrue(serializer.is_valid())
        self.assertIsInstance(serializer.save(), User)


class WorkdaySerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

        self.work1 = WorkdayFactory(user=self.user1)
        self.work2 = WorkdayFactory(user=self.user2)

    def test_workday_serialization(self):
        workdays = Workday.objects.all()

        # Single object serialization
        serializer = WorkdaySerializer(workdays[0])
        self.assertEqual(type(serializer), WorkdaySerializer)
        self.assertTrue(validate_json_schema("workday", serializer.data))

        # Muliple objects serialization
        serializer = WorkdaySerializer(workdays, many=True)
        self.assertEqual(type(serializer), WorkdaySerializer)
        self.assertEqual(len(serializer.data), 2)
        self.assertTrue(validate_json_schema("workdays", serializer.data))

    def test_workday_deserialization(self):
        UserFactory.create(username="joe")
        serializer = WorkdaySerializer(data={"user": "joe", 
                                             "start": "2014-03-13 09:30:07"})
        self.assertTrue(serializer.is_valid())
        self.assertIsInstance(serializer.save(), Workday)


#=============================================================================
# API Views Test Cases
#=============================================================================


class SuperuserEndpointsTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="admin", password="posma123", email="a@b.com")
        self.client = APIClient(enforce_csrf_checks=True)
        # self.client.login(username='admin', password="posma123")

        # authenticate using JWT
        response = self.client.post(reverse('login'),
                                    {"username": "admin", "password": "posma123"},
                                    format="json")
        token = response.data['token']
        self.assertTrue(token)
        self.auth = 'JWT {0}'.format(token)

    def test_authentication(self):
        self.assertTrue(self.auth)

    def test_user_list(self):
        # GET method
        UserFactory.create_batch(4)
        url = reverse('user_list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(validate_json_schema("users", response.data))
        self.assertEqual(len(response.data), 4)
        response = self.client.get(url)     # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # POST method
        self.client.post(url, {"username": "jackboot7",
                               "first_name": "Luis",
                               "last_name": "Santana",
                               "email": "luis.santana@gmail.com"}, HTTP_AUTHORIZATION=self.auth)
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(len(response.data), 5)
        response = self.client.post(url, {})    # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail(self):
        # GET method
        UserFactory(username="ospa", first_name="Oscar")
        url = reverse('user_detail', kwargs={'username': "ospa"})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(validate_json_schema("user", response.data))
        self.assertEqual(response.data['first_name'], "Oscar")
        response = self.client.get(url) # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT method
        response = self.client.put(url, {'username': "ospa", 'first_name': "Bob"}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Bob")
        response = self.client.put(url, {})     # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_workday_list(self):
        # POST method
        UserFactory.create(username="jackboot7")
        url = reverse('user_workday_list', kwargs={'username': "jackboot7"})
        response = self.client.post(url, {})    # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(url, {}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Invalid workday creation
        response = self.client.post(url, {}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

        # GET method
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(validate_json_schema("workdays", response.data))
        response = self.client.get(url)     # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_last_workday(self):
        # GET method
        user = UserFactory(username="cbruguera")
        WorkdayFactory.create(user=user)
        url = reverse('user_last_workday', kwargs={'username': "cbruguera"})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(validate_json_schema("workday", response.data))
        response = self.client.get(url)     # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT method
        response = self.client.put(url, {})     # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, {}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['finish'], datetime)

        # Invalid workday editing
        response = self.client.put(url, {}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_workday_list(self):
        # POST method
        UserFactory.create(username="cbruguera")
        url = reverse('workday_list')
        response = self.client.post(url, {})     # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(url, {'user': "cbruguera"}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Invalid workday creation
        response = self.client.post(url, {'user': "cbruguera"}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

        # GET method
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(validate_json_schema("workdays", response.data))
        response = self.client.get(url)     # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workday_detail(self):
        # GET method
        user = UserFactory.create(username="cbruguera")
        wd = WorkdayFactory(user=user)
        url = reverse('workday_detail', kwargs={'pk': wd.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(validate_json_schema("workday", response.data))
        response = self.client.get(url)     # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT method
        response = self.client.put(url, {'user': "cbruguera"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, {'user': "cbruguera"}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Invalid editing
        response = self.client.put(url, {'user': "cbruguera"}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)


class UserEndpointsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="non_admin", password="posma123", email="a@b.com")
        self.user.save()
        self.client = APIClient(enforce_csrf_checks=True)

        # authenticate using JWT
        response = self.client.post(reverse('login'),
                                    {"username": "non_admin", "password": "posma123"},
                                    format="json")
        token = response.data['token']
        self.assertTrue(token)
        self.auth = 'JWT {0}'.format(token)

    def test_authentication(self):
        self.assertTrue(self.auth)

    def test_user_list(self):
        # GET method (Unauthorized)
        UserFactory.create_batch(4)
        url = reverse('user_list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # POST method (Unauthorized)
        self.client.post(url, {"username": "jackboot7",
                               "first_name": "Luis",
                               "last_name": "Santana",
                               "email": "luis.santana@gmail.com"}, HTTP_AUTHORIZATION=self.auth)
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail(self):
        # Unauthorized access
        UserFactory(username="ospa", first_name="Oscar")
        url = reverse('user_detail', kwargs={'username': "ospa"})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # GET method
        url = reverse('user_detail', kwargs={'username': "non_admin"})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # PUT method
        response = self.client.put(url, {'username': "non_admin", 'first_name': "Bob"}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Bob")

    def test_user_workday_list(self):
        # Unauthorized access
        UserFactory.create(username="jackboot7")
        url = reverse('user_workday_list', kwargs={'username': "jackboot7"})
        response = self.client.post(url, {}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # POST method
        url = reverse('user_workday_list', kwargs={'username': "non_admin"})
        response = self.client.post(url, {}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Invalid workday creation
        response = self.client.post(url, {}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

        # GET method
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(validate_json_schema("workdays", response.data))
        response = self.client.get(url)     # Unauthorized access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_last_workday(self):
        # Unauthorized access
        UserFactory(username="cbruguera")
        url = reverse('user_last_workday', kwargs={'username': "cbruguera"})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # GET method
        WorkdayFactory.create(user=self.user)
        url = reverse('user_last_workday', kwargs={'username': "non_admin"})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(validate_json_schema("workday", response.data))

        # PUT method
        response = self.client.put(url, {}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['finish'], datetime)

        # Invalid workday editing
        response = self.client.put(url, {}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_workday_list(self):
        url = reverse('workday_list')
        # Unauthorized access
        response = self.client.post(url, {'user': "non_admin"}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # GET method (Unauthorized)
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workday_detail(self):
        # Unauthorized access
        user = UserFactory.create(username="cbruguera")
        wd = WorkdayFactory(user=user)
        url = reverse('workday_detail', kwargs={'pk': wd.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, {}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # GET method
        wd = WorkdayFactory(user=self.user)
        url = reverse('workday_detail', kwargs={'pk': wd.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(validate_json_schema("workday", response.data))

        # PUT method
        response = self.client.put(url, {'user': "non_admin"}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Invalid editing
        response = self.client.put(url, {'user': "non_admin"}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)
