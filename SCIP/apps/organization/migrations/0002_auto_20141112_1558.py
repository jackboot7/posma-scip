# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Employee',
        ),
        migrations.RenameField(
            model_name='workday',
            old_name='user',
            new_name='employee',
        ),
    ]
