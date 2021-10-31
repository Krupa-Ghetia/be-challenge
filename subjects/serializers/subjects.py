from rest_framework import serializers

from subjects.models import Subjects


class SubjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subjects
        fields = ['id', 'name', 'created_by']


class ValidateSubjectName(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=255)
