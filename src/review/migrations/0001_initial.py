# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(blank=True, max_length=20, null=True, verbose_name='Value', choices=[(b'5', b'5'), (b'4', b'4'), (b'3', b'3'), (b'2', b'2'), (b'1', b'1')])),
            ],
            options={
                'ordering': ['category', 'review'],
            },
        ),
        migrations.CreateModel(
            name='RatingCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.SlugField(max_length=32, verbose_name='Identifier', blank=True)),
                ('counts_for_average', models.BooleanField(default=True, verbose_name='Counts for average rating')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RatingCategoryChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=20, null=True, verbose_name='Value', blank=True)),
                ('ratingcategory', models.ForeignKey(related_name='choices', verbose_name='Rating category', to='review.RatingCategory')),
            ],
            options={
                'ordering': ('-value',),
            },
        ),
        migrations.CreateModel(
            name='RatingCategoryChoiceTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=128, verbose_name='Label')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='review.RatingCategoryChoice')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'review_ratingcategorychoice_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='RatingCategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('question', models.CharField(max_length=512, null=True, blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='review.RatingCategory')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'review_ratingcategory_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content', models.TextField(max_length=1024, verbose_name='Content', blank=True)),
                ('language', models.CharField(max_length=5, verbose_name='Language', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('average_rating', models.FloatField(default=0, verbose_name='Average rating')),
                ('extra_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('extra_content_type', models.ForeignKey(related_name='reviews_attached', blank=True, to='contenttypes.ContentType', null=True)),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='ReviewExtraInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=256, verbose_name='Type')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('review', models.ForeignKey(verbose_name='Review', to='review.Review')),
            ],
            options={
                'ordering': ['type'],
            },
        ),
        migrations.AddField(
            model_name='rating',
            name='category',
            field=models.ForeignKey(verbose_name='Category', to='review.RatingCategory'),
        ),
        migrations.AddField(
            model_name='rating',
            name='review',
            field=models.ForeignKey(related_name='ratings', verbose_name='Review', to='review.Review'),
        ),
        migrations.AlterUniqueTogether(
            name='ratingcategorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='ratingcategorychoicetranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
