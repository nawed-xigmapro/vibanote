# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-13 10:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0009_auto_20170613_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cms',
            name='testslug',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='test',
        ),
    ]
