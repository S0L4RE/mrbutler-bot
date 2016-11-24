# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.CharField(help_text='The snowflake ID of this guild from Discord', max_length=20, primary_key=True, serialize=False)),
                ('created_ts', models.DateTimeField(auto_now_add=True, verbose_name='Created Timestamp')),
                ('updated_ts', models.DateTimeField(auto_now=True, verbose_name='Updated Timestamp')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(help_text='The snowflake ID of this user from Discord', max_length=20, primary_key=True, serialize=False)),
                ('created_ts', models.DateTimeField(auto_now_add=True, verbose_name='Created Timestamp')),
                ('updated_ts', models.DateTimeField(auto_now=True, verbose_name='Updated Timestamp')),
            ],
        ),
    ]
