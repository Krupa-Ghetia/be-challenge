from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from datetime import datetime


from lessons.models import Lessons
from course.repository.course import CourseRepository


class LessonsRepository:
    @staticmethod
    def create_lesson(user, data):
        lesson = Lessons(name=data['name'], is_active=data['is_active'], created_by_id=user.id)
        lesson.save()

        for course_name in data['courses']:
            course = CourseRepository.get_course_by_name(course_name)
            lesson.courses.add(course)
        return lesson

    @staticmethod
    def lesson_already_exists(data):
        if Lessons.objects.filter(name=data['name']).exists():
            return True
        return False

    @staticmethod
    def get_lesson_by_id(lesson_id):
        return get_object_or_404(Lessons, id=lesson_id)

    @staticmethod
    def get_lessons_by_course(course_id, user):
        try:
            lessons = Lessons.objects.filter(courses__id=course_id)
        except ObjectDoesNotExist:
            raise Http404("Lesson object does not exist")

        if not user.is_instructor:
            lessons = lessons.filter(is_active=True)
            return lessons
        return lessons

    @staticmethod
    def get_lesson_by_course_and_lesson_id(course_id, lesson_id):
        return get_object_or_404(Lessons, courses__id=course_id, id=lesson_id)

    @staticmethod
    def get_all_lessons(user):
        lessons = Lessons.objects.all()
        if not user.is_instructor:
            lessons = lessons.filter(is_active=True)
            return lessons
        return lessons

    @staticmethod
    def update_lesson_name(lesson, data):
        lesson.name = data['name']
        lesson.row_last_updated = datetime.now()
        lesson.save()
        return lesson

    @staticmethod
    def update_lesson_active_status(lesson, data):
        lesson.is_active = data['is_active']
        lesson.row_last_updated = datetime.now()
        lesson.save()
        return lesson

    @staticmethod
    def update_lesson_courses(lesson, data):
        for course_name in data['courses']:
            course = CourseRepository.get_course_by_name(course_name)
            lesson.courses.add(course)
        lesson.row_last_updated = datetime.now()
        return lesson
