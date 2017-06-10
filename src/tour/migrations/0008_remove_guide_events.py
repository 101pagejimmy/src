# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0007_auto_20170521_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='events',
        ),
    ]
