from django.db import models

from model_utils.models import TimeStampedModel
from django_extensions.db.fields import ShortUUIDField

from accounts.models import User
from streams.models import Stream
from core.utils import id_generator


class Question(TimeStampedModel):
    user = models.ForeignKey(User, related_name="questions")
    stream = models.ForeignKey(Stream, related_name="questions", null=True, blank=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = id_generator()

        return super(Question, self).save(*args, **kwargs)


class Choice(TimeStampedModel):
    uuid = ShortUUIDField(db_index=True)
    question = models.ForeignKey(Question, related_name="choices")

    title = models.CharField(max_length=255)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.title
