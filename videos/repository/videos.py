from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from datetime import datetime

from videos.models import Videos
from tags.repository.tags import TagRepository
from lessons.repository.lessons import LessonsRepository


class VideoRepository:

    @staticmethod
    def video_already_exists(data):
        if Videos.objects.filter(title=data['title']).exists():
            return True
        return False

    @staticmethod
    def create_video(user, data):
        video = Videos(title=data['title'], link=data['link'], is_active=data['is_active'], created_by_id=user.id)
        video.save()

        for tag_name in data['tags']:
            tag = TagRepository.get_or_create_tag(tag_name, user)
            video.tags.add(tag)

        for lesson_name in data['lessons']:
            lesson = LessonsRepository.get_lesson_by_name(lesson_name)
            video.lessons.add(lesson)
        return video

    @staticmethod
    def get_video_by_id(video_id):
        video = get_object_or_404(Videos, id=video_id)
        return video

    @staticmethod
    def get_all_videos():
        videos = Videos.objects.all()
        return videos

    @staticmethod
    def update_video_title(video, data):
        video.title = data['title']
        video.row_last_updated = datetime.now()
        video.save()
        return video

    @staticmethod
    def update_video_link(video, data):
        video.link = data['link']
        video.row_last_updated = datetime.now()
        video.save()
        return video

    @staticmethod
    def update_video_active_status(video, data):
        video.is_active = data['is_active']
        video.row_last_updated = datetime.now()
        video.save()
        return video

    @staticmethod
    def update_video_tags(video, data, user):
        for tag_name in data['tags']:
            tag = TagRepository.get_or_create_tag(tag_name, user)
            video.tags.add(tag)
        video.row_last_updated = datetime.now()
        return video

    @staticmethod
    def update_video_lessons(video, data):
        for lesson_name in data['lessons']:
            lesson = LessonsRepository.get_lesson_by_name(lesson_name)
            video.lessons.add(lesson)
        video.row_last_updated = datetime.now()
        return video
