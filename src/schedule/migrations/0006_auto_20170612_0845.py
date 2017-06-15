# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_event_reservation_spots_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence',
            name='spots_free',
            field=models.IntegerField(null=True, default=0),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='spots_total',
            field=models.IntegerField(verbose_name='spots', null=True, default=0),
        ),
        migrations.AlterField(
            model_name='event',
            name='reservation_spots_total',
            field=models.IntegerField(verbose_name='spots', blank=True, null=True, choices=[(5, 5), (10, 10), (15, 15), (20, 20), (25, 25), (30, 30), (35, 35), (50, 50)]),
        ),
    ]
