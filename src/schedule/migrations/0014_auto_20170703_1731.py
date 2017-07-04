# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0013_event_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='fk',
            field=models.ForeignKey(default=1, to='tour.Guide'),
        ),
    ]
