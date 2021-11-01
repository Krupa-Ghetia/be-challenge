from rest_framework import serializers

from tags.models import Tags


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ['id', 'name', 'created_by']


class ValidateTagName(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=128)