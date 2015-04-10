# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('millipays', '0003_cart_cashlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='member',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='cashlog',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cashlog',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
