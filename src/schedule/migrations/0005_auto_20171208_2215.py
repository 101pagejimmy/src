# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20171208_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='price',
            field=models.DecimalField(default=0.0, verbose_name='price', max_digits=100, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='sale_price',
            field=models.DecimalField(null=True, verbose_name='sale_price', max_digits=20, decimal_places=2, blank=True),
        ),
    ]
