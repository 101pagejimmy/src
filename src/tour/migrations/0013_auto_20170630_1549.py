# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0012_auto_20170630_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='occurrence',
            field=models.ForeignKey(blank=True, null=True, default=1, to='schedule.Occurrence'),
        ),
    ]
