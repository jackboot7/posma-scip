# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djcelery', '__first__'),
        ('organization', '0004_auto_20141217_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgsettings',
            name='reminder_task',
            field=models.ForeignKey(related_name='+', blank=True, to='djcelery.PeriodicTask', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orgsettings',
            name='checkout_task',
            field=models.ForeignKey(related_name='+', blank=True, to='djcelery.PeriodicTask', null=True),
            preserve_default=True,
        ),
    ]
