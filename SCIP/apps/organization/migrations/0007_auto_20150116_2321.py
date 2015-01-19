# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20150116_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workday',
            name='staff_notes',
            field=models.TextField(max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workday',
            name='user_notes',
            field=models.TextField(max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
    ]
