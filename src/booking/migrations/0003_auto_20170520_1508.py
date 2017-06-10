# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20170509_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_status',
            field=models.ForeignKey(verbose_name='Booking status', blank=True, null=True, to='booking.BookingStatus'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='gender',
            field=models.CharField(verbose_name='Gender', max_length=10, blank=True, choices=[('mrs', 'Mrs'), ('mr', 'Mr')]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='notes',
            field=models.TextField(verbose_name='Notes', max_length=1024, blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='time_unit',
            field=models.CharField(verbose_name='Time unit', max_length=64, blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='booking',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=10, blank=True, choices=[('dr', 'Dr.'), ('prof', 'Prof.')]),
        ),
    ]
