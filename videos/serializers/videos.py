from rest_framework import serializers

from videos.models import Videos
from tags.serializers.tags import TagSerializer
from lessons.serializers.lessons import LessonsSerializer


class VideoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    lessons = LessonsSerializer(read_only=True, many=True)

    class Meta:
        model = Videos
        fields = ['id', 'title', 'link', 'is_active', 'created_by', 'tags', 'lessons']


class VideoDtoSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=255, allow_null=False, allow_blank=False)
    link = serializers.URLField(allow_blank=False, allow_null=False)
    is_active = serializers.BooleanField(default=True)
    tags = serializers.ListField(allow_empty=True, allow_null=False)
    lessons = serializers.ListField(allow_empty=True, allow_null=False)


class ValidateVideoTitle(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=255, allow_null=False, allow_blank=False)


class ValidateVideoLink(serializers.Serializer):
    link = serializers.URLField(allow_blank=False, allow_null=False)


class ValidateVideoActiveStatus(serializers.Serializer):
    is_active = serializers.BooleanField(default=True)


class ValidateVideoTags(serializers.Serializer):
    tags = serializers.ListField(allow_empty=True, allow_null=False)


class ValidateVideoLessons(serializers.Serializer):
    lessons = serializers.ListField(allow_empty=True, allow_null=False)