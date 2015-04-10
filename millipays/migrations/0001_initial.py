# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nick', models.CharField(max_length=20)),
                ('number', models.CharField(max_length=13)),
                ('balance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('number', models.CharField(max_length=13)),
                ('price', models.FloatField()),
                ('stock', models.IntegerField()),
                ('imageName', models.CharField(max_length=20)),
            ],
        ),
    ]
