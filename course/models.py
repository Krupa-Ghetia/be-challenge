from django.db import models
from datetime import datetime

from users.models import User
from subjects.models import Subjects


class Course(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subjects)
    row_created = models.DateTimeField(default=datetime.now)
    row_last_updated = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
