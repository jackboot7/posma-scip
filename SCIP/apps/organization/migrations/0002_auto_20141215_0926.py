# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_checkout_time', models.TimeField(default=datetime.datetime(2000, 1, 1, 18, 0))),
                ('scheduled_verification_time', models.TimeField(default=datetime.datetime(2000, 1, 1, 20, 0))),
                ('checkout_reminder_time', models.TimeField(default=datetime.datetime(2000, 1, 1, 19, 0))),
            ],
            options={
                'verbose_name_plural': 'Settings',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='workday',
            name='start',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
