# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_auto_20150130_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='workday',
            name='location',
            field=geoposition.fields.GeopositionField(max_length=42, null=True, blank=True),
            preserve_default=True,
        ),
    ]
