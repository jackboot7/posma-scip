from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from djcelery.models import TaskState, WorkerState, PeriodicTask, IntervalSchedule, CrontabSchedule

from apps.organization.models import Profile, Workday, OrgSettings


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'


class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )


class OrgSettingsAdmin(admin.ModelAdmin):
    exclude = ('checkout_task', 'reminder_task')


class WorkdayAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'finish', 'user_notes', 'staff_notes')


admin.site.register(OrgSettings, OrgSettingsAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Workday, WorkdayAdmin)

admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)
