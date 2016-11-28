# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CompaniesApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='photo',
            field=models.ImageField(default=0, upload_to='static/companyimages'),
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.CharField(default='/', max_length=300),
        ),
    ]
