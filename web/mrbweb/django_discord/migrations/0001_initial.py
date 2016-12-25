# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(help_text='The snowflake ID of this user from Discord', max_length=20, primary_key=True, serialize=False)),
                ('username', models.CharField(help_text='The username for this user', max_length=32)),
                ('discriminator', models.CharField(help_text='The 4-digit discord-tag for this user', max_length=4)),
                ('avatar', models.CharField(help_text="The user's avatar hash", max_length=255)),
                ('is_bot', models.BooleanField(help_text='Is this Discord user a bot?', verbose_name='Bot User')),
                ('created_ts', models.DateTimeField(auto_now_add=True, help_text='The timestamp for when this object was created', verbose_name='Created Timestamp')),
                ('updated_ts', models.DateTimeField(auto_now=True, help_text='The timestamp for when this object was updated', verbose_name='Updated Timestamp')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.CharField(help_text='The snowflake ID of this guild from Discord', max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The name for this guild', max_length=100)),
                ('owner', models.ForeignKey(help_text="The user that owns this guild", on_delete=django.db.models.deletion.CASCADE, related_name='servers', to='django_discord.User')),
                ('icon', models.CharField(help_text="The guild's icon hash value", max_length=255)),
                ('created_ts', models.DateTimeField(auto_now_add=True, help_text='The timestamp for when this object was created', verbose_name='Created Timestamp')),
                ('updated_ts', models.DateTimeField(auto_now=True, help_text='The timestamp for when this object was updated', verbose_name='Updated Timestamp')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
