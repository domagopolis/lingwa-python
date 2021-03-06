# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-02-27 03:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lingwa', '0012_url_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='UtterenceUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lingwa.Url')),
                ('utterence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lingwa.Utterence')),
            ],
        ),
    ]
