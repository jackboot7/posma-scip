from django.contrib import auth
from rest_framework import serializers

from apps.organization.models import *


class WorkdaySerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField() #format="%Y-%m-%d %H:%M:%S"
    finish = serializers.DateTimeField()
    user = serializers.CharField(source="user.username")
    hours_worked = serializers.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        model = Workday
        fields = ('start', 'finish', 'user', 'hours_worked')


class UserSerializer(serializers.ModelSerializer):
    last_workday = serializers.SerializerMethodField('get_last_workday')
    is_working = serializers.SerializerMethodField('get_is_working')
    average_hours_worked = serializers.SerializerMethodField('get_avg_hours_worked')

    class Meta:
        model = auth.models.User
        fields = ('username', 'first_name', 'last_name', 'email', 'last_workday', 'is_working', 'average_hours_worked')

    def get_last_workday(self, obj):
        latest = Workday.objects.user(obj.username).latest('start')
        serial = WorkdaySerializer(latest)
        serial.fields.pop('user', None)
        return serial.data

    def get_is_working(self, obj):
        latest = Workday.objects.user(obj.username).latest('start')
        return latest.finish is None

    def get_avg_hours_worked(self, obj):
        workdays = obj.workday_set.all()
        accum = 0.0
        cont = 0

        for wd in workdays:
            if wd.hours_worked:
                accum = accum + wd.hours_worked
                cont = cont + 1

        return accum / cont
