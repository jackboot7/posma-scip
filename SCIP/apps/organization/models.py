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
        return self.filter(user__username=login)


class Profile(models.Model):
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
            existing = Profile.objects.get(user=self.user)
            self.id = existing.id   # force update instead of insert
        except Profile.DoesNotExist:
            pass
        models.Model.save(self, *args, **kwargs)

    @receiver(post_save, sender=auth.models.User)
    def create_profile(sender, instance, created, **kwargs):
        """
        Method receives signal in order to create corresponding Profile everytime  auth.models.User is created
        """
        if created:
            Profile.objects.get_or_create(user=instance)


class Workday(models.Model):
    """
    A workday represents a succesful session of work, delimited by 'start' and 'finish' timestamps.
    """
    user = models.ForeignKey(auth.models.User)
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
        if self.finish is not None and self.start > self.finish:
            raise ValidationError("Workday start time can't be greater than finish time")

        overlapping = Workday.objects.user(self.user.username).exclude(
            id=self.id).filter(start__range=(self.start, self.finish))
        overlapping2 = Workday.objects.user(self.user.username).exclude(
            id=self.id).filter(finish__range=(self.start, self.finish))

        if overlapping.exists() or overlapping2.exists():
            raise ValidationError("Specified user has already worked in the given datetime range")

    def __unicode__(self):
        return "%s: %s - %s" % (self.user.username, self.start, self.finish)