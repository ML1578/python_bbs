# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-05-27 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTagRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('tag_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]