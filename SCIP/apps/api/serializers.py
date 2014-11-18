from django.contrib import auth
from rest_framework import serializers

from apps.organization import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = auth.Models.User


class WorkdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workday
