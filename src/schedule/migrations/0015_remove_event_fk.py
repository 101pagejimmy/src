# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0014_auto_20170703_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='fk',
        ),
    ]
