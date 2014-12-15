import datetime

from django.db import models
from django.contrib import auth
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError


#===============================================================================
# Custom Model Managers
#===============================================================================

class WorkdayManager(models.Manager):
    """
    Custom manager for the Workday class
    """
    def user(self, login):
        """
        Limit queryset results by specific user
        """
        try:
            user = auth.models.User.objects.get(username=login)
        except auth.models.User.DoesNotExist:
            raise
        return self.filter(user=user)


#===============================================================================
# Application Model Classes
#===============================================================================


class OrgSettings(models.Model):
    """
    Relevant settings related to a particular organization
    """
    default_checkout_time = models.TimeField(default=datetime.time(18, 0))
    scheduled_verification_time = models.TimeField(default=datetime.time(20, 0))
    checkout_reminder_time = models.TimeField(default=datetime.time(19, 0))

    class Meta:
        verbose_name_plural = "Settings"
        verbose_name = "settings"

    def save(self, *args, **kwargs):
        # Removes all other entries if there are any
        self.__class__.objects.exclude(id=self.id).delete()
        super(OrgSettings, self).save(*args, **kwargs)


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
    start = models.DateTimeField(auto_now_add=True)
    finish = models.DateTimeField(blank=True, null=True)

    # model manager
    objects = WorkdayManager()

    class Meta:
        ordering = ['-start']

    @property
    def hours_worked(self):
        if self.finish:
            diff = self.finish - self.start
            return diff.total_seconds() / 60 / 60
        else:
            return None

    def clean(self):
        """
        Self validation method
        """
        if self.finish is not None and self.start > self.finish:
            raise ValidationError("Workday start time can't be greater than finish time")

        try:
            latest = Workday.objects.user(self.user.username).exclude(id=self.id).latest('start')
            if not latest.finish:
                raise ValidationError("Latest workday hasn't finished yet for given user")
        except Workday.DoesNotExist:
            pass

        overlapping = Workday.objects.user(self.user.username).exclude(
            id=self.id).filter(start__range=(self.start, self.finish))
        overlapping2 = Workday.objects.user(self.user.username).exclude(
            id=self.id).filter(finish__range=(self.start, self.finish))

        if overlapping.exists() or overlapping2.exists():
            raise ValidationError("Specified user has already worked in the given datetime range")

    def __unicode__(self):
        return "%s: %s - %s" % (self.user.username, self.start, self.finish)
