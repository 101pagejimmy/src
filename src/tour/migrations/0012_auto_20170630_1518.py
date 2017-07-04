# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0012_auto_20170612_1024'),
        ('tour', '0011_guide_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='event',
        ),
        migrations.AddField(
            model_name='guide',
            name='occurrence',
            field=models.ForeignKey(blank=True, null=True, to='schedule.Occurrence'),
        ),
    ]
