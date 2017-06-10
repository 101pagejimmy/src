# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_text_fields_not_null'),
        ('tour', '0006_auto_20170521_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guide',
            name='events',
        ),
        migrations.AddField(
            model_name='guide',
            name='events',
            field=models.ManyToManyField(verbose_name='events', blank=True, null=True, related_name='events', to='schedule.Event'),
        ),
    ]
