# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0016_event_guide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='guide',
            field=models.ForeignKey(blank=True, null=True, to='tour.Guide'),
        ),
    ]
