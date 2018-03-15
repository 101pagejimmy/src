# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import schedule.models.events


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20180228_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.TextField(verbose_name='City', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=schedule.models.events.upload_location, blank=True),
        ),
    ]
