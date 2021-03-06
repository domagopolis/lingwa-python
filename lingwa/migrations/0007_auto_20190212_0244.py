# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-12 02:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lingwa', '0006_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='LexicalDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='keywordlexicalclass',
            name='keyword',
        ),
        migrations.RemoveField(
            model_name='keywordlexicalclass',
            name='lexical_class',
        ),
        migrations.AlterModelOptions(
            name='lexicalclass',
            options={'verbose_name': 'lexical class', 'verbose_name_plural': 'lexical classes'},
        ),
        migrations.AddField(
            model_name='lexicalclass',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lingwa.LexicalClass'),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='url',
            name='last_read',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='utterence',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='KeywordLexicalClass',
        ),
        migrations.AddField(
            model_name='lexicaldefinition',
            name='keyword',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lingwa.Keyword'),
        ),
        migrations.AddField(
            model_name='lexicaldefinition',
            name='lexical_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lingwa.LexicalClass'),
        ),
        migrations.AddField(
            model_name='lexicaldefinition',
            name='translations',
            field=models.ManyToManyField(related_name='_lexicaldefinition_translations_+', to='lingwa.LexicalDefinition'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='lexical_definitions',
            field=models.ManyToManyField(through='lingwa.LexicalDefinition', to='lingwa.LexicalClass'),
        ),
    ]
