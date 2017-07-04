# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0016_auto_20170702_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='occurrence',
        ),
    ]
