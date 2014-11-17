from django.db import models
from django.contrib import auth
from django.dispatch import receiver
from django.db.models.signals import post_save
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
    birthday = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Little hack to allow user creation via Admin inline form and still keep the post_save signal
        """
        try:
            existing = Employee.objects.get(user=self.user)
            self.id = existing.id   # force update instead of insert
        except Employee.DoesNotExist:
            pass
        models.Model.save(self, *args, **kwargs)

    @receiver(post_save, sender=auth.models.User)
    def create_employee(sender, instance, created, **kwargs):
        """
        Method receives signal in order to create corresponding Employee everytime  auth.models.User is created
        """
        if created:
            Employee.objects.get_or_create(user=instance)


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
