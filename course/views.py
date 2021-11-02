from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from course.repository.course import CourseRepository
from course.serializers.course import (
    CourseSerializer, CourseDtoSerializer, CourseSubscriptionSerializer, ValidateSubscriptionStatus,
    ValidateCourseName, ValidateCourseActiveStatus, ValidateCourseSubjects,)
from users.utils import user_is_instructor, user_is_author


class CourseView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, subject=None, pk=None):
        try:
            if pk:
                course = CourseRepository.get_course_by_id(pk)
                course = CourseRepository.update_course_view_count(course)
                serializer = CourseSerializer(course)
            elif subject:
                courses = CourseRepository.get_courses_by_subject(subject, request.user)
                serializer = CourseSerializer(courses, many=True)
            else:
                courses = CourseRepository.get_all_courses(request.user)
                serializer = CourseSerializer(courses, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'courses': serializer.data
                }
            )

        except Http404 as e:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'errors': 'Course does not exist!'
                }
            )
        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'errors': e
                }
            )

    def post(self, request):
        if not user_is_instructor(request.user):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an instructur to add new courses"
                }
            )

        serializer = CourseDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        validated_data = serializer.validated_data

        try:
            if CourseRepository.course_already_exists(validated_data):
                return Response(
                    status=status.HTTP_409_CONFLICT,
                    data={
                        "msg": "Course already exists!"
                    }
                )
            course = CourseRepository.create_course(request.user, validated_data)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'id': course.id,
                }
            )

        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )

    def put(self, request, pk):
        course = CourseRepository.get_course_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, course):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an authorized instructur to update the course"
                }
            )

        try:
            # Update course name
            if 'name' in request.data:
                serializer = ValidateCourseName(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data = serializer.validated_data

                if CourseRepository.course_already_exists(validated_data):
                    return Response(
                        status=status.HTTP_409_CONFLICT,
                        data={
                            "msg": "Course already exists!"
                        }
                    )
                course = CourseRepository.update_course_name(course, validated_data)

            # Update course active status
            if 'is_active' in request.data:
                serializer = ValidateCourseActiveStatus(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data = serializer.validated_data

                course = CourseRepository.update_course_active_status(course, validated_data)

            # Add course subjects
            if 'subjects' in request.data:
                serializer = ValidateCourseSubjects(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data = serializer.validated_data

                course = CourseRepository.update_course_subjects(course, request.user, validated_data)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'id': course.id,
                }
            )
        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )

    def delete(self, request, pk):
        course = CourseRepository.get_course_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, course):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an authorized instructur to delete the course"
                }
            )

        try:
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )


class CourseAnalyticsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if not user_is_instructor(request.user):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an instructur to view analytics"
                }
            )

        try:
            courses = CourseRepository.get_most_viewed_courses()
            serializer = CourseSerializer(courses, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'courses': serializer.data
                }
            )
        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'errors': e
                }
            )


class CourseSubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            subscribed_courses = CourseRepository.get_subscribed_courses(request.user)
            serializer = CourseSubscriptionSerializer(subscribed_courses, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'courses': serializer.data
                }
            )
        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'errors': e
                }
            )

    def post(self, request):
        serializer = ValidateSubscriptionStatus(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        validated_data = serializer.validated_data

        try:
            course_id = request.query_params.get('course_id')
            course_subscription = CourseRepository.subscribe_unsubscribe_course(course_id, request.user, validated_data)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'id': course_subscription.id,
                }
            )

        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )
