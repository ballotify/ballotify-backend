# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('user_agent', models.CharField(max_length=255, blank=True)),
                ('ip', models.CharField(max_length=255, blank=True)),
                ('question', models.ForeignKey(related_name='votes', to='questions.Question')),
                ('user', models.ForeignKey(related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='VoteChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('choice', models.ForeignKey(related_name='vote_choices', to='questions.Choice')),
                ('user', models.ForeignKey(related_name='vote_choices', to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(related_name='choices', to='votes.Vote')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='votechoice',
            unique_together=set([('vote', 'choice', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('question', 'user')]),
        ),
    ]
