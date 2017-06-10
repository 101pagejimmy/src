# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0005_guide_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='events',
            field=models.ForeignKey(verbose_name='events', blank=True, null=True, related_name='events', to='schedule.Event'),
        ),
    ]
