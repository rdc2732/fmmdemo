# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-25 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fmm', '0002_testfeature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testfeature',
            name='dependency',
        ),
        migrations.AddField(
            model_name='testfeature',
            name='dependency',
            field=models.ManyToManyField(to='fmm.TestFeature'),
        ),
    ]
