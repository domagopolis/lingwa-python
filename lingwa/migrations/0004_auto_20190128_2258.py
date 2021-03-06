# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-28 22:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lingwa', '0003_keywordurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordLexicalClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lingwa.Keyword')),
            ],
        ),
        migrations.CreateModel(
            name='LexicalClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='keywordlexicalclass',
            name='lexical_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lingwa.LexicalClass'),
        ),
    ]
