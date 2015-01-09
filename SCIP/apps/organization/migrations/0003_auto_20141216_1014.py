# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('djcelery', '__first__'),
        ('organization', '0002_auto_20141215_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orgsettings',
            options={'verbose_name': 'Settings', 'verbose_name_plural': 'Settings'},
        ),
        migrations.AddField(
            model_name='orgsettings',
            name='periodic_task',
            field=models.ForeignKey(blank=True, to='djcelery.PeriodicTask', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orgsettings',
            name='checkout_reminder_time',
            field=models.TimeField(default=datetime.time(19, 0)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orgsettings',
            name='default_checkout_time',
            field=models.TimeField(default=datetime.time(18, 0)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orgsettings',
            name='scheduled_verification_time',
            field=models.TimeField(default=datetime.time(20, 0)),
            preserve_default=True,
        ),
    ]
