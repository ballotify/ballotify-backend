# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='is_multiple',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
