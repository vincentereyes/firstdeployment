# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-27 04:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userd', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='received_msgs', to='userd.User'),
            preserve_default=False,
        ),
    ]
