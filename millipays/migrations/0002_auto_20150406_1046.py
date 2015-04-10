# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('millipays', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='number',
            new_name='barcode',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='imageName',
            new_name='name',
        ),
        migrations.AddField(
            model_name='product',
            name='member_discount',
            field=models.FloatField(default=0.5),
        ),
    ]
