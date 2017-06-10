# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guidebooking',
            name='booking',
        ),
        migrations.AlterField(
            model_name='guide',
            name='tourSize',
            field=models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]),
        ),
        migrations.DeleteModel(
            name='GuideBooking',
        ),
    ]
