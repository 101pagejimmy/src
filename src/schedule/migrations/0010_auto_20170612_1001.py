# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_auto_20170612_0936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='occurrence',
            old_name='spots_total',
            new_name='reservation_spots',
        ),
        migrations.AlterField(
            model_name='event',
            name='reservation_spots',
            field=models.IntegerField(verbose_name='reservation_spots', blank=True, null=True, db_index=True, choices=[(5, 5), (10, 10), (15, 15), (20, 20), (25, 25), (30, 30), (35, 35), (50, 50)], help_text='How large is your tour group?'),
        ),
    ]
