# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-13 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0007_cms'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='reason',
            field=models.TextField(null=True),
        ),
    ]
