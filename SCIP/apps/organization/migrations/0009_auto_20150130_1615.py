# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_auto_20150119_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='workday',
            name='user_agent',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workday',
            name='start',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
