# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('millipays', '0005_member_prepaid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='prepaid',
            new_name='addPrepaid',
        ),
    ]
