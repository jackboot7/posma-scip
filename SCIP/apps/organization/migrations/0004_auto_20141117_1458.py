# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20141112_1600'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workday',
            options={'ordering': ['-start']},
        ),
        migrations.AddField(
            model_name='employee',
            name='birthday',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
