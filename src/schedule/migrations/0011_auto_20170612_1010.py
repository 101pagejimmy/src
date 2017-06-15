# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0010_auto_20170612_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='reservation_spots',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
