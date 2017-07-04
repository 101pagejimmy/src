# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0015_guide_occurrence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='occurrence',
            field=models.ForeignKey(blank=True, null=True, to='schedule.Occurrence'),
        ),
    ]
