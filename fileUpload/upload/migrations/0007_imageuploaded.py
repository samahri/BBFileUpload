# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_auto_20170502_0535'),
    ]

    operations = [
        migrations.CreateModel(
            name='imageUploaded',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_pic', models.ImageField(default='none', upload_to='images/')),
            ],
        ),
    ]
