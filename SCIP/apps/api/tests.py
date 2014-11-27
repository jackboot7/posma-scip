import json
from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from jsonschema import validate

from apps.api.serializers import *
from apps.api.views import *


#=============================================================================
# Serializers Test Cases
#=============================================================================


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="burrg",
                                         first_name="Carlos",
                                         last_name="Bruguera",
                                         email="burrg@harrb.gov",
                                         password="posma123")
        self.user2 = User.objects.create(username="ospa",
                                         first_name="Oscar",
                                         last_name="Parales",
                                         email="ospa@ospa.gov",
                                         password="posma123")
        self.user3 = User.objects.create(username="jackboot7",
                                         first_name="Luis",
                                         last_name="Santana",
                                         email="luis.santana@gmail.com",
                                         password="posma123")

    def test_user_schema(self):
        serializer = UserSerializer(self.user1)
        json_data = JSONRenderer().render(serializer.data)
        user_schema = open("apps/api/schemas/user.json").read()
        try:
            validate(json.loads(json_data), json.loads(user_schema))
            is_valid = True
        except ValidationError:
            is_valid = False

        self.assertTrue(is_valid)

    def test_users_schema(self):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        json_data = JSONRenderer().render(serializer.data)
        users_schema = open("apps/api/schemas/users.json").read()
        try:
            validate(json.loads(json_data), json.loads(users_schema))
            is_valid = True
        except ValidationError:
            is_valid = False

        self.assertTrue(is_valid)


class WorkdaySerializerTestCase(TestCase):
    def setUp(self):
        self.now = datetime.utcnow()
        self.now = self.now.replace(tzinfo=pytz.utc)

        self.user1 = User.objects.create(username="burrg",
                                         first_name="Carlos",
                                         last_name="Bruguera",
                                         email="burrg@harrb.gov",
                                         password="posma123")
        self.user2 = User.objects.create(username="ospa",
                                         first_name="Oscar",
                                         last_name="Parales",
                                         email="ospa@ospa.gov",
                                         password="posma123")
        self.work1 = Workday.objects.create(user=self.user1, start=self.now)
        self.work2 = Workday.objects.create(user=self.user2, start=self.now)

    def test_workday_schema(self):
        serializer = WorkdaySerializer(self.work1)
        json_data = JSONRenderer().render(serializer.data)
        workday_schema = open("apps/api/schemas/workday.json").read()
        try:
            validate(json.loads(json_data), json.loads(workday_schema))
            # update finish time and validate again
            self.work1.finish = self.now + timedelta(hours=9)
            serializer = WorkdaySerializer(self.work1)
            json_data = JSONRenderer().render(serializer.data)
            validate(json.loads(json_data), json.loads(workday_schema))
            is_valid = True
        except ValidationError:
            is_valid = False

        self.assertTrue(is_valid)

    def test_workdays_schema(self):
        workdays = Workday.objects.all()
        serializer = WorkdaySerializer(workdays, many=True)
        json_data = JSONRenderer().render(serializer.data)
        workdays_schema = open("apps/api/schemas/workdays.json").read()
        try:
            validate(json.loads(json_data), json.loads(workdays_schema))
            is_valid = True
        except ValidationError:
            is_valid = False

        self.assertTrue(is_valid)

#=============================================================================
# API Views Test Cases
#=============================================================================
