# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0008_auto_20170612_0931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='reservation_spots_total',
        ),
        migrations.AddField(
            model_name='event',
            name='reservation_spots',
            field=models.IntegerField(verbose_name='reservation_spots', blank=True, null=True, choices=[(5, 5), (10, 10), (15, 15), (20, 20), (25, 25), (30, 30), (35, 35), (50, 50)]),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='spots_free',
            field=models.IntegerField(null=True, default=35),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='spots_total',
            field=models.IntegerField(verbose_name='reservation_spots', null=True),
        ),
    ]
