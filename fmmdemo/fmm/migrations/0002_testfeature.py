# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-25 17:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fmm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('selection_name', models.CharField(blank=True, max_length=100)),
                ('rule_type', models.CharField(blank=True, choices=[('CHO', 'choice'), ('SEL', 'selection')], max_length=15)),
                ('option_min', models.IntegerField(blank=True, null=True)),
                ('option_max', models.IntegerField(blank=True, null=True)),
                ('enabled', models.NullBooleanField(default=False)),
                ('selected', models.NullBooleanField(default=False)),
                ('dependency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fmm.TestFeature')),
            ],
        ),
    ]
