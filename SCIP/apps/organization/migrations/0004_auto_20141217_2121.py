# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20141216_1014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orgsettings',
            old_name='periodic_task',
            new_name='checkout_task',
        ),
        migrations.AlterField(
            model_name='orgsettings',
            name='checkout_reminder_time',
            field=models.TimeField(default=datetime.time(23, 30)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orgsettings',
            name='default_checkout_time',
            field=models.TimeField(default=datetime.time(22, 30)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orgsettings',
            name='scheduled_verification_time',
            field=models.TimeField(default=datetime.time(0, 30)),
            preserve_default=True,
        ),
    ]
