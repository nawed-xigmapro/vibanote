# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-16 07:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0039_auto_20170816_0537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='is_from_deleted',
        ),
        migrations.RemoveField(
            model_name='messages',
            name='is_to_deleted',
        ),
    ]