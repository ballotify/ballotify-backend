import uuid
from django.db import models

from model_utils.models import TimeStampedModel
from shortuuid import ShortUUID

from accounts.models import User
from streams.models import Stream


class QuestionQueryset(models.QuerySet):
    def public(self):
        return self.filter(is_private=False)


class Question(TimeStampedModel):
    user = models.ForeignKey(User, related_name="questions")
    stream = models.ForeignKey(Stream, related_name="questions", null=True, blank=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    is_anonymous = models.BooleanField(default=False)
    is_multiple = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_randomized = models.BooleanField(default=False)

    objects = QuestionQueryset.as_manager()

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ShortUUID().random(length=10)

        return super(Question, self).save(*args, **kwargs)


class Choice(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, related_name="choices")

    title = models.CharField(max_length=255)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.title
