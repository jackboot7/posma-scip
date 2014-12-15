from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from apps.organization.models import Profile, Workday, Settings


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'


class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )


admin.site.register(Settings)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Workday)
