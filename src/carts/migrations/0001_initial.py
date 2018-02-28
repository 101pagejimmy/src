# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('subtotal', models.DecimalField(default=25.0, max_digits=50, decimal_places=2)),
                ('tax_percentage', models.DecimalField(default=0.085, max_digits=10, decimal_places=5)),
                ('tax_total', models.DecimalField(default=25.0, max_digits=50, decimal_places=2)),
                ('total', models.DecimalField(default=25.0, max_digits=50, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('line_item_total', models.DecimalField(max_digits=10, decimal_places=2)),
                ('cart', models.ForeignKey(to='carts.Cart')),
            ],
        ),
    ]
