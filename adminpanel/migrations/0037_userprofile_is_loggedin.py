# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-07 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0036_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_loggedin',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
