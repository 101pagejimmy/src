# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20170612_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='reservation_spots_total',
            field=models.IntegerField(verbose_name='reservation_spots_total', blank=True, null=True, choices=[(5, 5), (10, 10), (15, 15), (20, 20), (25, 25), (30, 30), (35, 35), (50, 50)]),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='spots_total',
            field=models.IntegerField(verbose_name='reservation_spots_total', null=True, default=0),
        ),
    ]
