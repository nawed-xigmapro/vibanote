# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-16 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0038_remove_messages_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='is_from_deleted',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='messages',
            name='is_to_deleted',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
