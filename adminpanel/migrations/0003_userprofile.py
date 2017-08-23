# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-12 07:10
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminpanel', '0002_auto_20170612_0708'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('gender', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True)),
                ('picture', models.ImageField(null=True, upload_to='media')),
                ('medium_pic', models.CharField(max_length=200, null=True)),
                ('thumbnail_pic', models.CharField(max_length=200, null=True)),
                ('isfeatured', models.IntegerField(blank=True, null=True)),
                ('address', models.TextField(null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=200, null=True)),
                ('country', models.CharField(max_length=200, null=True)),
                ('website', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('activateit', models.IntegerField(blank=True, null=True)),
                ('forgotstr', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
