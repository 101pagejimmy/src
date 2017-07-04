# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0013_auto_20170630_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='occurrence',
        ),
    ]
