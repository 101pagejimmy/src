# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0018_guide_occurrence'),
        ('schedule', '0015_remove_event_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='guide',
            field=models.ForeignKey(default=1, to='tour.Guide'),
        ),
    ]
