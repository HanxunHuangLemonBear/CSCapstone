# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 03:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CompaniesApp', '0002_auto_20161128_1548'),
        ('ProjectsApp', '0002_auto_20161128_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CompaniesApp.Company'),
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='programmingLanguage',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='speciality',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='yearsOfExperience',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
