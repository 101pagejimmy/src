# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0018_guide_occurrence'),
        ('schedule', '0012_auto_20170612_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='fk',
            field=models.ForeignKey(default=datetime.datetime(2017, 7, 4, 0, 31, 0, 724645, tzinfo=utc), to='tour.Guide'),
            preserve_default=False,
        ),
    ]
