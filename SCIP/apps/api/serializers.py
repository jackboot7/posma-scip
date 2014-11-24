import pytz
from datetime import datetime

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.organization.models import *


class WorkdaySerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(required=False)     # format="%Y-%m-%d %H:%M:%S"
    finish = serializers.DateTimeField(required=False)
    user = serializers.SlugRelatedField(many=False, read_only=False, slug_field='username')
    hours_worked = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)

    class Meta:
        model = Workday
        fields = ('id', 'user', 'start', 'finish', 'hours_worked')

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        utcnow = datetime.utcnow()
        utcnow = utcnow.replace(tzinfo=pytz.utc)

        if instance:
            # Update existing instance
            instance.finish = utcnow
            username = attrs.get('user', instance.user)
            if username:
                user = auth.models.User.objects.get(username=username)
                instance.user = user

            return instance

        # Create new instance
        username = attrs.get('user', "")
        user = auth.models.User.objects.get(username=username)
        attrs['user'] = user
        attrs['start'] = utcnow
        wd = Workday(**attrs)
        return wd


class UserSerializer(serializers.ModelSerializer):
    last_workday = serializers.SerializerMethodField('get_last_workday')
    is_working = serializers.SerializerMethodField('get_is_working')
    average_hours_worked = serializers.SerializerMethodField('get_avg_hours_worked')

    class Meta:
        model = auth.models.User
        fields = ('username', 'first_name', 'last_name', 'email', 'last_workday', 'is_working', 'average_hours_worked')

    def get_last_workday(self, obj):
        try:
            latest = Workday.objects.user(obj.username).latest('start')
            serial = WorkdaySerializer(latest)
            serial.fields.pop('user', None)
            return serial.data
        except ObjectDoesNotExist:
            return {}

    def get_is_working(self, obj):
        try:
            latest = Workday.objects.user(obj.username).latest('start')
            return latest.finish is None
        except ObjectDoesNotExist:
            return False

    def get_avg_hours_worked(self, obj):
        workdays = obj.workday_set.all()
        accum = 0.0
        cont = 0

        for wd in workdays:
            if wd.hours_worked:
                accum = accum + wd.hours_worked
                cont = cont + 1

        return accum / cont if cont > 0 else 0
