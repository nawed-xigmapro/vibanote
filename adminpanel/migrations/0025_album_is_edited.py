# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0024_tracks'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='is_edited',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
