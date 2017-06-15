# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_text_fields_not_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='reservation_spots_total',
            field=models.IntegerField(blank=True, null=True, choices=[(5, 5), (10, 10), (15, 15), (20, 20), (25, 25), (30, 30), (35, 35), (50, 50)]),
        ),
    ]
