from django.db import models
from datetime import datetime

from users.models import User


class Subjects(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    row_created = models.DateTimeField(default=datetime.now)
    row_last_updated = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
