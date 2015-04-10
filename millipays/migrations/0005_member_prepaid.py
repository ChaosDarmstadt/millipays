# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('millipays', '0004_auto_20150408_0415'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='prepaid',
            field=models.FloatField(default=0),
        ),
    ]
