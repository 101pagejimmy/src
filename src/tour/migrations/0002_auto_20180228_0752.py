# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='living',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='guide',
            name='remember',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
