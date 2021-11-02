from django.shortcuts import get_object_or_404
from datetime import datetime

from tags.models import Tags


class TagRepository:

    @staticmethod
    def tag_already_exists(data):
        if Tags.objects.filter(name=data['name']).exists():
            return True
        return False

    @staticmethod
    def create_tag(user, data):
        tag = Tags(name=data['name'], created_by_id=user.id)
        tag.save()
        return tag

    @staticmethod
    def get_or_create_tag(tag_name, user):
        if Tags.objects.filter(name=tag_name).exists():
            return Tags.objects.get(name=tag_name)
        tag = Tags.objects.create(name=tag_name, created_by_id=user.id)
        return tag

    @staticmethod
    def get_tag_by_id(tag_id):
        tag = get_object_or_404(Tags, id=tag_id)
        return tag

    @staticmethod
    def get_all_tags():
        tags = Tags.objects.all()
        return tags

    @staticmethod
    def update_tag_name(tag, data):
        tag.name = data['name']
        tag.row_last_updated = datetime.now()
        tag.save()
        return tag
