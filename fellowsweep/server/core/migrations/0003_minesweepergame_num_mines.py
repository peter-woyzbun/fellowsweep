# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_minesweepergame_won'),
    ]

    operations = [
        migrations.AddField(
            model_name='minesweepergame',
            name='num_mines',
            field=models.IntegerField(default=10),
        ),
    ]
