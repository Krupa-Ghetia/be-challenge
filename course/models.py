from django.db import models
from datetime import datetime

from users.models import User
from subjects.models import Subjects


class Course(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subjects)
    row_created = models.DateTimeField(default=datetime.now)
    row_last_updated = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class CourseSubscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    has_subscribed = models.BooleanField(default=True)
    row_created = models.DateTimeField(default=datetime.now)
    row_last_updated = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Course_subscription'
        verbose_name_plural = 'Courses_subscription'
