# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-05 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0067_unit_extensions'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicenodeunitcount',
            name='city_as_department',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
