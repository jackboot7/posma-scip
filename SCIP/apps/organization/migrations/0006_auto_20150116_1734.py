# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20141217_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='workday',
            name='edited',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workday',
            name='staff_notes',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workday',
            name='user_notes',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
