# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0007_projecttag_tagtype'),
        ('GroupsApp', '0004_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='tag',
            field=models.ManyToManyField(blank=True, to='ProjectsApp.projectTag'),
        ),
    ]
