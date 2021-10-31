from django.db import models
from datetime import datetime

from users.models import User
from course.models import Course


class Lessons(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    row_created = models.DateTimeField(default=datetime.now)
    row_last_updated = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
