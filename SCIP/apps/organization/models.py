from django.db import models
from django.contrib import auth
from django.core.exceptions import ValidationError


class WorkdayManager(models.Manager):
    """
    Custom manager for the Workday class
    """
    def user(self, login):
        """
        Limit queryset results by specific user
        """
        return self.filter(employee__user__username=login)


class Employee(models.Model):
    """
    Application user class.
    """
    user = models.OneToOneField(auth.models.User)


class Workday(models.Model):
    """
    A workday represents a succesful session of work, delimited by 'start' and 'finish' timestamps.
    """
    employee = models.ForeignKey(Employee)
    start = models.DateTimeField()
    finish = models.DateTimeField(blank=True, null=True)

    # model manager
    objects = WorkdayManager()

    class Meta:
        ordering = ['-start']

    def clean(self):
        """
        Self validation method
        """
        if self.start > self.finish:
            raise ValidationError("Workday start time can't be greater than finish time")

        overlapping = Workday.objects.user(self.employee.user.username).exclude(
            id=self.id).filter(start__range=(self.start, self.finish))
        overlapping2 = Workday.objects.user(self.employee.user.username).exclude(
            id=self.id).filter(finish__range=(self.start, self.finish))

        if overlapping.exists() or overlapping2.exists():
            raise ValidationError("Specified user has already worked in the given datetime range")
