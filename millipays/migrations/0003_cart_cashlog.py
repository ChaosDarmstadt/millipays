# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('millipays', '0002_auto_20150406_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('member', models.ForeignKey(to='millipays.Member')),
                ('products', models.ManyToManyField(to='millipays.Product')),
            ],
        ),
        migrations.CreateModel(
            name='CashLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('purchase_date', models.DateTimeField(verbose_name='date purchased')),
                ('member', models.ForeignKey(to='millipays.Member')),
                ('product', models.ForeignKey(to='millipays.Product')),
            ],
        ),
    ]
