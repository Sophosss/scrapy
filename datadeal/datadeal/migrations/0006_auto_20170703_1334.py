# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-03 13:34
from __future__ import unicode_literals
from django.contrib.postgres.operations import HStoreExtension
import django.contrib.postgres.fields.hstore
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datadeal', '0005_remove_variable_important'),
    ]

    operations = [
        HStoreExtension(),
        migrations.CreateModel(
            name='SpiderData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scrapyname', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('uid', models.CharField(max_length=50, verbose_name='uid')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('data', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'verbose_name': '\u6570\u636e\u4fe1\u606f',
                'verbose_name_plural': '\u6570\u636e\u4fe1\u606f\u7ba1\u7406',
            },
        ),
        migrations.AlterField(
            model_name='scrapylist',
            name='priority',
            field=models.IntegerField(default=10, help_text=b'\xe5\x80\xbc\xe8\xb6\x8a\xe5\xb0\x8f\xe8\xb6\x8a\xe4\xbc\x98\xe5\x85\x88', verbose_name='\u9879\u76ee\u4f18\u5148\u7ea7'),
        ),
    ]
