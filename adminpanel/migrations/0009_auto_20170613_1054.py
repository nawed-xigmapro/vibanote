# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-13 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0008_userprofile_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='cms',
            name='testslug',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='test',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]