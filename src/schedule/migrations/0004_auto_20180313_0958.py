# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20180301_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='latitude',
            field=models.DecimalField(decimal_places=10, max_digits=50, blank=True, null=True, verbose_name='latitude', db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='longitude',
            field=models.DecimalField(decimal_places=10, max_digits=50, blank=True, null=True, verbose_name='longitude', db_index=True),
        ),
        migrations.AlterIndexTogether(
            name='occurrence',
            index_together=set([('latitude', 'longitude'), ('start', 'end')]),
        ),
    ]
