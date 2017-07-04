# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0017_auto_20170703_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='guide',
        ),
    ]
