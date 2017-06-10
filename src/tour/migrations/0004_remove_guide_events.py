# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0003_guide_events'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='events',
        ),
    ]
