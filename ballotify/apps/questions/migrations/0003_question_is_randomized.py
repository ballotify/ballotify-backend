# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20150905_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_randomized',
            field=models.BooleanField(default=False),
        ),
    ]
