from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
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