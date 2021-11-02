from django.contrib import admin

from .models import Course, CourseSubscription


admin.site.register(Course)
admin.site.register(CourseSubscription)
