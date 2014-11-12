# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20141112_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workday',
            name='finish',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
