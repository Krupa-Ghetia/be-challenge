from rest_framework import serializers

from course.models import Course, CourseSubscription
from subjects.serializers.subjects import SubjectsSerializer


class CourseSerializer(serializers.ModelSerializer):
    subjects = SubjectsSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'is_active', 'view_count', 'created_by', 'subjects']


class CourseSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSubscription
        fields = ['id', 'course', 'user', 'has_subscribed']


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


class ValidateSubscriptionStatus(serializers.Serializer):
    has_subscribed = serializers.BooleanField(default=False)
