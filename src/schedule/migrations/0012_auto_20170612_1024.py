# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_auto_20170612_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='reservation_spots',
            field=models.IntegerField(verbose_name='reservation_spots', null=True),
        ),
    ]
