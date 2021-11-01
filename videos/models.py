from django.db import models
from datetime import datetime

from users.models import User
from lessons.models import Lessons
from tags.models import Tags


class Videos(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, unique=True)
    link = models.URLField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    lessons = models.ManyToManyField(Lessons)
    row_created = models.DateTimeField(default=datetime.now)
    row_last_updated = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'