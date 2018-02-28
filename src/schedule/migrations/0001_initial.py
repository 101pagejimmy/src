# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(max_length=200, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'calendar',
                'verbose_name_plural': 'calendar',
            },
        ),
        migrations.CreateModel(
            name='CalendarRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('distinction', models.CharField(max_length=20, verbose_name='distinction')),
                ('inheritable', models.BooleanField(default=True, verbose_name='inheritable')),
                ('calendar', models.ForeignKey(verbose_name='calendar', to='schedule.Calendar')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'calendar relation',
                'verbose_name_plural': 'calendar relations',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(verbose_name='start', db_index=True)),
                ('end', models.DateTimeField(help_text='The end time must be later than the start time.', verbose_name='end', db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('reservation_spots', models.IntegerField(choices=[(5, 5), (10, 10), (15, 15), (20, 20), (25, 25), (30, 30), (35, 35), (50, 50)], blank=True, help_text='How large is your tour group?', null=True, verbose_name='reservation_spots', db_index=True)),
                ('price', models.DecimalField(default=0.0, max_digits=100, decimal_places=2)),
                ('sale_price', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('location', models.CharField(max_length=200, blank=True, help_text='Where does the tour meetup? Please enter like such. 331 NW 26th St, Corvallis OR, 97330', null=True, verbose_name='location_point', db_index=True)),
                ('latitude', models.DecimalField(null=True, max_digits=50, decimal_places=10, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=50, decimal_places=10, blank=True)),
                ('tour_type', models.CharField(choices=[('Boat', 'Boat'), ('Bike', 'Bike'), ('Walk', 'Walk')], max_length=255, blank=True, help_text='What type of tour is this?', null=True, verbose_name='tour_type', db_index=True)),
                ('tour_icon', models.CharField(max_length=255, null=True, verbose_name='tour_icon', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('end_recurring_period', models.DateTimeField(help_text='This date is ignored for one time only events.', null=True, verbose_name='end recurring period', db_index=True, blank=True)),
                ('color_event', models.CharField(max_length=10, verbose_name='Color event', blank=True)),
                ('calendar', models.ForeignKey(verbose_name='calendar', blank=True, to='schedule.Calendar', null=True)),
                ('creator', models.ForeignKey(related_name='creator', verbose_name='creator', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='EventRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('distinction', models.CharField(max_length=20, verbose_name='distinction')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('event', models.ForeignKey(verbose_name='event', to='schedule.Event')),
            ],
            options={
                'verbose_name': 'event relation',
                'verbose_name_plural': 'event relations',
            },
        ),
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('end', models.DateTimeField(verbose_name='end', db_index=True)),
                ('cancelled', models.BooleanField(default=False, verbose_name='cancelled')),
                ('original_start', models.DateTimeField(verbose_name='original start')),
                ('original_end', models.DateTimeField(verbose_name='original end')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('reservation_spots', models.IntegerField(null=True, verbose_name='reservation_spots')),
                ('spots_free', models.IntegerField(default=35, null=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('price', models.DecimalField(default=0.0, verbose_name='price', max_digits=100, decimal_places=2)),
                ('sale_price', models.DecimalField(null=True, verbose_name='sale_price', max_digits=20, decimal_places=2, blank=True)),
                ('start', models.DateTimeField(verbose_name='start', db_index=True)),
                ('latitude', models.DecimalField(null=True, verbose_name='latitude', max_digits=50, decimal_places=10, blank=True)),
                ('longitude', models.DecimalField(null=True, verbose_name='longitude', max_digits=50, decimal_places=10, blank=True)),
                ('tour_type', models.CharField(max_length=255, verbose_name='tour_type', blank=True)),
                ('tour_icon', models.CharField(max_length=255, null=True, verbose_name='tour_icon', blank=True)),
                ('sail', models.NullBooleanField(default=False, verbose_name='sail')),
                ('bike', models.NullBooleanField(default=False, verbose_name='bike')),
                ('trail', models.NullBooleanField(default=False, verbose_name='trail')),
                ('event', models.ForeignKey(verbose_name='event', to='schedule.Event')),
                ('guide', models.ForeignKey(related_name='guide', blank=True, to='tour.Guide', null=True)),
            ],
            options={
                'verbose_name': 'occurrence',
                'verbose_name_plural': 'occurrences',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('frequency', models.CharField(max_length=10, verbose_name='frequency', choices=[('YEARLY', 'Yearly'), ('MONTHLY', 'Monthly'), ('WEEKLY', 'Weekly'), ('DAILY', 'Daily'), ('HOURLY', 'Hourly'), ('MINUTELY', 'Minutely'), ('SECONDLY', 'Secondly')])),
                ('params', models.TextField(verbose_name='params', blank=True)),
            ],
            options={
                'verbose_name': 'rule',
                'verbose_name_plural': 'rules',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='rule',
            field=models.ForeignKey(blank=True, to='schedule.Rule', help_text="Select '----' for a one time only event.", null=True, verbose_name='rule'),
        ),
        migrations.AlterIndexTogether(
            name='occurrence',
            index_together=set([('start', 'end')]),
        ),
        migrations.AlterIndexTogether(
            name='event',
            index_together=set([('start', 'end')]),
        ),
    ]
