# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-16 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0044_auto_20170816_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='is_new_thread',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
    ]
