from django.contrib import auth
from rest_framework import serializers

from apps.organization.models import *


class WorkdaySerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    finish = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    user = serializers.CharField(source="user.username")

    class Meta:
        model = Workday
        fields = ('start', 'finish', 'user')


class UserSerializer(serializers.ModelSerializer):
    last_workday = serializers.SerializerMethodField('get_last_workday')

    class Meta:
        model = auth.models.User
        fields = ('username', 'first_name', 'last_name', 'email', 'last_workday')

    def get_last_workday(self, obj):
        latest = Workday.objects.user(obj.username).latest('start')
        serial = WorkdaySerializer(latest)
        serial.fields.pop('user', None)
        return serial.data
