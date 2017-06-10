# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_libs.models_mixins
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(blank=True, max_length=10, verbose_name='Gender', choices=[(b'mrs', 'Mrs'), (b'mr', 'Mr')])),
                ('title', models.CharField(blank=True, max_length=10, verbose_name='Title', choices=[(b'dr', 'Dr.'), (b'prof', 'Prof.')])),
                ('forename', models.CharField(max_length=20, verbose_name='First name', blank=True)),
                ('surname', models.CharField(max_length=20, verbose_name='Last name', blank=True)),
                ('nationality', django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='Nationality')),
                ('street1', models.CharField(max_length=256, verbose_name='Street 1', blank=True)),
                ('street2', models.CharField(max_length=256, verbose_name='Street 2', blank=True)),
                ('city', models.CharField(max_length=256, verbose_name='City', blank=True)),
                ('zip_code', models.CharField(max_length=256, verbose_name='ZIP/Postal code', blank=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='Country')),
                ('email', models.EmailField(max_length=254, verbose_name='Email', blank=True)),
                ('phone', models.CharField(max_length=256, verbose_name='Phone', blank=True)),
                ('special_request', models.TextField(max_length=1024, verbose_name='Special request', blank=True)),
                ('date_from', models.DateTimeField(null=True, verbose_name='From', blank=True)),
                ('date_until', models.DateTimeField(null=True, verbose_name='Until', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('booking_id', models.CharField(max_length=100, verbose_name='Booking ID', blank=True)),
                ('notes', models.TextField(max_length=1024, verbose_name=b'Notes', blank=True)),
                ('time_period', models.PositiveIntegerField(null=True, verbose_name='Time period', blank=True)),
                ('time_unit', models.CharField(default=b'', max_length=64, verbose_name='Time unit', blank=True)),
                ('total', models.DecimalField(null=True, verbose_name='Total', max_digits=36, decimal_places=2, blank=True)),
                ('currency', models.CharField(max_length=128, verbose_name='Currency', blank=True)),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='BookingError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=1000, verbose_name='Message', blank=True)),
                ('details', models.TextField(max_length=4000, verbose_name='Details', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('booking', models.ForeignKey(verbose_name='Booking', to='booking.Booking')),
            ],
        ),
        migrations.CreateModel(
            name='BookingItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('persons', models.PositiveIntegerField(null=True, verbose_name='Persons', blank=True)),
                ('subtotal', models.DecimalField(null=True, verbose_name='Subtotal', max_digits=36, decimal_places=2, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('booking', models.ForeignKey(verbose_name='Booking', to='booking.Booking')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-booking__creation_date'],
            },
        ),
        migrations.CreateModel(
            name='BookingStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(verbose_name='Slug')),
            ],
            options={
                'abstract': False,
            },
            bases=(django_libs.models_mixins.TranslationModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BookingStatusTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='booking.BookingStatus')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'booking_bookingstatus_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ExtraPersonInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forename', models.CharField(max_length=20, verbose_name='First name')),
                ('surname', models.CharField(max_length=20, verbose_name='Last name')),
                ('arrival', models.DateTimeField(null=True, verbose_name='Arrival', blank=True)),
                ('message', models.TextField(max_length=1024, verbose_name='Message', blank=True)),
                ('booking', models.ForeignKey(verbose_name='Booking', to='booking.Booking')),
            ],
            options={
                'ordering': ['-booking__creation_date'],
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_status',
            field=models.ForeignKey(verbose_name=b'Booking status', blank=True, to='booking.BookingStatus', null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='session',
            field=models.ForeignKey(verbose_name='Session', blank=True, to='sessions.Session', null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(related_name='bookings', verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='bookingstatustranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
