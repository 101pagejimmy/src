# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0018_guide_occurrence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='occurrence',
        ),
    ]
