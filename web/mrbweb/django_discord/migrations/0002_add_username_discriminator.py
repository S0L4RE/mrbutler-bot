# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_discord', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='discriminator',
            field=models.CharField(
                default='',
                help_text='The 4-digit discord-tag for this user',
                max_length=4
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(
                default='',
                help_text='The username for this user',
                max_length=50
            ),
            preserve_default=False,
        ),
    ]
