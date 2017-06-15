# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20170612_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='spots_free',
            field=models.IntegerField(null=True, default='reservation_spots_total'),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='spots_total',
            field=models.IntegerField(verbose_name='reservation_spots_total', null=True),
        ),
    ]
