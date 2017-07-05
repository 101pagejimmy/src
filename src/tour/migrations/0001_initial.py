# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import tour.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(max_length=1000)),
                ('tourSize', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('tour_description', models.TextField(max_length=1000)),
                ('remember', models.TextField(max_length=1000, blank=True, null=True)),
                ('living', models.CharField(max_length=100, blank=True, null=True)),
                ('secondary_language', models.CharField(max_length=100, blank=True, null=True, choices=[('English', 'English'), ('Spanish', 'Spanish'), ('Russian', 'Russian'), ('Italian', 'Italian')])),
                ('meet_up_point', models.CharField(max_length=1000, blank=True, null=True)),
                ('height_field', models.IntegerField(default=100)),
                ('width_field', models.IntegerField(default=80)),
                ('language', models.CharField(max_length=20, choices=[('English', 'English'), ('Spanish', 'Spanish'), ('Russian', 'Russian'), ('Italian', 'Italian')])),
                ('updated', models.DateTimeField(null=True, auto_now=True)),
                ('timestamp', models.DateTimeField(null=True, auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
                ('guide_name', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GuideImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('image', models.ImageField(upload_to=tour.models.image_upload_to)),
                ('guide', models.ForeignKey(to='tour.Guide')),
            ],
        ),
    ]
