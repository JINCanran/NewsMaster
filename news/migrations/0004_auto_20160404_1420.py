# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20160403_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomesticNewsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='InternationalNewsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='MainNewsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('data', models.CharField(max_length=100)),
                ('abstract', models.CharField(max_length=10000)),
                ('url', models.CharField(max_length=1000)),
                ('mediaurl', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='NewsDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('data', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('source', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=10000)),
                ('url', models.CharField(max_length=1000)),
                ('mediaurl', models.CharField(max_length=1000)),
            ],
        ),
        migrations.DeleteModel(
            name='Detail',
        ),
        migrations.DeleteModel(
            name='News',
        ),
    ]
