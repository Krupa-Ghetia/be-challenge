from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


from course.models import Course, CourseSubscription
from subjects.repository.subjects import SubjectsRepository


class CourseRepository:

    @staticmethod
    def create_course(user, data):
        course = Course(name=data['name'], is_active=data['is_active'], created_by_id=user.id)
        course.save()

        for subject_name in data['subjects']:
            subject = SubjectsRepository.get_or_create_subject(user, subject_name)
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
    def get_course_by_name(course_name):
        try:
            course = Course.objects.get(name=course_name)
            return course
        except ObjectDoesNotExist:
            raise Http404('Course does not exist')

    @staticmethod
    def get_courses_by_subject(subject_id, user):
        try:
            courses = Course.objects.filter(subjects__id=subject_id)
        except ObjectDoesNotExist:
            raise Http404("Subject does not exist")

        if not user.is_instructor:
            courses = courses.filter(is_active=True)
            return courses
        return courses

    @staticmethod
    def get_course_by_subject_and_course_id(subject_id, course_id):
        return get_object_or_404(Course, subjects__id=subject_id, id=course_id)

    @staticmethod
    def get_all_courses(user):
        courses = Course.objects.all()

        if not user.is_instructor:
            courses = courses.filter(is_active=True)
            return courses
        return courses

    @staticmethod
    def get_most_viewed_courses():
        return Course.objects.filter(view_count__gt=0).order_by('-view_count')

    @staticmethod
    def update_course_name(course, data):
        course.name = data['name']
        course.row_last_updated = datetime.now()
        course.save()
        return course

    @staticmethod
    def update_course_active_status(course, data):
        course.is_active = data['is_active']
        course.row_last_updated = datetime.now()
        course.save()
        return course

    @staticmethod
    def update_course_subjects(course, user, data):
        for subject_name in data['subjects']:
            subject = SubjectsRepository.get_or_create_subject(user, subject_name)
            course.subjects.add(subject)
        course.row_last_updated = datetime.now()
        course.save()
        return course

    @staticmethod
    def update_course_view_count(course):
        course.view_count += 1
        course.row_last_updated = datetime.now()
        course.save()
        return course

    @staticmethod
    def get_subscribed_courses(user):
        subscribed_courses = CourseSubscription.objects.filter(user_id=user.id, has_subscribed=True)
        return subscribed_courses

    @staticmethod
    def subscribe_unsubscribe_course(course_id, user, data):
        if CourseSubscription.objects.filter(course_id=course_id, user_id=user.id).exists():
            subscribed_course = CourseSubscription.objects.get(course_id=course_id, user_id=user.id)
            subscribed_course.has_subscribed = data['has_subscribed']
            subscribed_course.row_last_updated = datetime.now()
            subscribed_course.save()
        else:
            subscribed_course = CourseSubscription(course_id=course_id, user_id=user.id,
                                                   has_subscribed=data['has_subscribed'])
            subscribed_course.save()

        return subscribed_course
