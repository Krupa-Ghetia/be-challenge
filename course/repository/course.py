from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import datetime

from course.models import Course
from subjects.repository.subjects import SubjectsRepository


class CourseRepository:

    @staticmethod
    def create_course(user, data):
        course = Course(name=data['name'], is_active=data['is_active'], created_by_id=user.id)
        course.save()

        for subject_name in data['subjects']:
            subject, status = SubjectsRepository.get_or_create_subject(user, subject_name)
            course.subjects.add(subject)
        return course

    @staticmethod
    def course_already_exists(data):
        if Course.objects.filter(name=data['name']).exists():
            return True
        return False

    @staticmethod
    def get_course_by_id(course_id):
        return get_object_or_404(Course, id=course_id)

    @staticmethod
    def get_courses_by_subject(subject_id):
        return get_list_or_404(Course, subjects__id=subject_id)

    @staticmethod
    def get_course_by_subject_and_course_id(subject_id, course_id):
        return get_object_or_404(Course, subjects__id=subject_id, id=course_id)

    @staticmethod
    def get_all_courses():
        return Course.objects.all()

    @staticmethod
    def update_course_name(course, data):
        course.name = data['name']
        course.save()
        return course

    @staticmethod
    def update_course_active_status(course, data):
        course.is_active = data['is_active']
        course.save()
        return course

    @staticmethod
    def update_course_subjects(course, user, data):
        for subject_name in data['subjects']:
            subject, status = SubjectsRepository.get_or_create_subject(user, subject_name)
            course.subjects.add(subject)
        return course

