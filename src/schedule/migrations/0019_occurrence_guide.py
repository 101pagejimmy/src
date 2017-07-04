# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0019_remove_guide_occurrence'),
        ('schedule', '0018_remove_event_guide'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence',
            name='guide',
            field=models.ForeignKey(blank=True, null=True, related_name='guide', to='tour.Guide'),
        ),
    ]
