# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0012_auto_20170612_1024'),
        ('tour', '0014_remove_guide_occurrence'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='occurrence',
            field=models.ForeignKey(blank=True, null=True, default=1, to='schedule.Occurrence'),
        ),
    ]
