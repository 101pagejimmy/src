# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence',
            name='bike',
            field=models.NullBooleanField(default=False, verbose_name='sail'),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='sail',
            field=models.NullBooleanField(default=False, verbose_name='sail'),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='trail',
            field=models.NullBooleanField(default=False, verbose_name='sail'),
        ),
    ]
