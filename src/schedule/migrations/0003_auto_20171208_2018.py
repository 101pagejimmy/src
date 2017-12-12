# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20171013_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.DecimalField(default=0.0, max_digits=100, decimal_places=2),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='price',
            field=models.DecimalField(default=0.0, max_digits=100, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='bike',
            field=models.NullBooleanField(default=False, verbose_name='bike'),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='trail',
            field=models.NullBooleanField(default=False, verbose_name='trail'),
        ),
    ]
