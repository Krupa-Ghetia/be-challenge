from rest_framework import serializers

from course.models import Course
from subjects.serializers.subjects import SubjectsSerializer


class CourseSerializer(serializers.ModelSerializer):
    subjects = SubjectsSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'is_active', 'created_by', 'subjects']


class CourseDtoSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=255)
    is_active = serializers.BooleanField(default=True)
    subjects = serializers.ListField(allow_empty=True)


class ValidateCourseName(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=255)


class ValidateCourseActiveStatus(serializers.Serializer):
    is_active = serializers.BooleanField(default=True)


class ValidateCourseSubjects(serializers.Serializer):
    subjects = serializers.ListField(allow_empty=True)
