from rest_framework import serializers

from lessons.models import Lessons
from course.serializers.course import CourseSerializer


class LessonsSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(read_only=True, many=True)

    class Meta:
        model = Lessons
        fields = ['id', 'name', 'is_active', 'created_by', 'courses']


class LessonsDtoSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=255)
    is_active = serializers.BooleanField(default=True)
    courses = serializers.ListField(allow_empty=True)


class ValidateLessonName(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=255)


class ValidateLessonActiveStatus(serializers.Serializer):
    is_active = serializers.BooleanField(default=True)


class ValidateLessonCourses(serializers.Serializer):
    courses = serializers.ListField(allow_empty=True)
