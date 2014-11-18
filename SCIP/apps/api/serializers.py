from rest_framework import serializers
from apps.organization import models


class EmployeeSerializer(serializers.ModelSerializer):  # Employee ?
    class Meta:
        model = models.Employee


class WorkdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workday
