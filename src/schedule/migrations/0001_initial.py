# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tour', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=200)),
                ('slug', models.SlugField(verbose_name='slug', max_length=200)),
            ],
            options={
                'verbose_name': 'calendar',
                'verbose_name_plural': 'calendar',
            },
        ),
        migrations.CreateModel(
            name='CalendarRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.IntegerField()),
                ('distinction', models.CharField(verbose_name='distinction', max_length=20)),
                ('inheritable', models.BooleanField(verbose_name='inheritable', default=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('start', models.DateTimeField(verbose_name='start', db_index=True)),
                ('end', models.DateTimeField(verbose_name='end', db_index=True, help_text='The end time must be later than the start time.')),
                ('title', models.CharField(verbose_name='title', max_length=255)),
                ('reservation_spots', models.IntegerField(verbose_name='reservation_spots', blank=True, null=True, db_index=True, choices=[(5, 5), (10, 10), (15, 15), (20, 20), (25, 25), (30, 30), (35, 35), (50, 50)], help_text='How large is your tour group?')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('created_on', models.DateTimeField(verbose_name='created on', auto_now_add=True)),
                ('updated_on', models.DateTimeField(verbose_name='updated on', auto_now=True)),
                ('end_recurring_period', models.DateTimeField(verbose_name='end recurring period', blank=True, null=True, db_index=True, help_text='This date is ignored for one time only events.')),
                ('color_event', models.CharField(verbose_name='Color event', max_length=10, blank=True)),
                ('calendar', models.ForeignKey(verbose_name='calendar', blank=True, null=True, to='schedule.Calendar')),
                ('creator', models.ForeignKey(verbose_name='creator', blank=True, null=True, related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='EventRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.IntegerField()),
                ('distinction', models.CharField(verbose_name='distinction', max_length=20)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=255, blank=True)),
                ('reservation_spots', models.IntegerField(verbose_name='reservation_spots', null=True)),
                ('spots_free', models.IntegerField(null=True, default=35)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('start', models.DateTimeField(verbose_name='start', db_index=True)),
                ('end', models.DateTimeField(verbose_name='end', db_index=True)),
                ('cancelled', models.BooleanField(verbose_name='cancelled', default=False)),
                ('original_start', models.DateTimeField(verbose_name='original start')),
                ('original_end', models.DateTimeField(verbose_name='original end')),
                ('created_on', models.DateTimeField(verbose_name='created on', auto_now_add=True)),
                ('updated_on', models.DateTimeField(verbose_name='updated on', auto_now=True)),
                ('event', models.ForeignKey(verbose_name='event', to='schedule.Event')),
                ('guide', models.ForeignKey(blank=True, null=True, related_name='guide', to='tour.Guide')),
            ],
            options={
                'verbose_name': 'occurrence',
                'verbose_name_plural': 'occurrences',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=32)),
                ('description', models.TextField(verbose_name='description')),
                ('frequency', models.CharField(verbose_name='frequency', max_length=10, choices=[('YEARLY', 'Yearly'), ('MONTHLY', 'Monthly'), ('WEEKLY', 'Weekly'), ('DAILY', 'Daily'), ('HOURLY', 'Hourly'), ('MINUTELY', 'Minutely'), ('SECONDLY', 'Secondly')])),
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
            field=models.ForeignKey(verbose_name='rule', blank=True, null=True, help_text="Select '----' for a one time only event.", to='schedule.Rule'),
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
