# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import schedule.models.events


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(height_field='height_field', width_field='width_field', null=True, upload_to=schedule.models.events.upload_location, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(help_text='The end time must be later than the start time.', verbose_name='End', db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=200, blank=True, help_text='Where does the tour meetup? Please enter like such. 331 NW 26th St, Corvallis OR, 97330', null=True, verbose_name='Location Point', db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='reservation_spots',
            field=models.IntegerField(choices=[(5, 5), (10, 10), (15, 15), (20, 20), (25, 25), (30, 30), (35, 35), (50, 50)], blank=True, help_text='How large is your tour group?', null=True, verbose_name='Reservation Spots', db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name='Start', db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='event',
            name='tour_type',
            field=models.CharField(choices=[('Boat', 'Boat'), ('Bike', 'Bike'), ('Walk', 'Walk')], max_length=255, blank=True, help_text='What type of tour is this?', null=True, verbose_name='Meetup Location', db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='end',
            field=models.DateTimeField(verbose_name='End', db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='reservation_spots',
            field=models.IntegerField(null=True, verbose_name='Reservation Spots'),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='sale_price',
            field=models.DecimalField(null=True, verbose_name='Sale Price', max_digits=20, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='start',
            field=models.DateTimeField(verbose_name='Start', db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title', blank=True),
        ),
    ]
