from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
import logging

from lessons.repository.lessons import LessonsRepository
from lessons.serializers.lessons import (
    LessonsSerializer, LessonsDtoSerializer, ValidateLessonName, ValidateLessonActiveStatus, ValidateLessonCourses)
from users.utils import user_is_instructor, user_is_author

logger = logging.getLogger('be_challenge')


class LessonView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, course=None, pk=None):
        logger.info(f"Request:GET Model:Lesson")
        try:
            if pk:
                lesson = LessonsRepository.get_lesson_by_id(pk)
                serializer = LessonsSerializer(lesson)
            elif course:
                lessons = LessonsRepository.get_lessons_by_course(course, request.user)
                serializer = LessonsSerializer(lessons, many=True)
            else:
                lessons = LessonsRepository.get_all_lessons(request.user)
                serializer = LessonsSerializer(lessons, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'lessons': serializer.data
                }
            )

        except Http404 as e:
            logger.error("Request:GET Model:Lesson Errors: Lesson does not exist")
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'errors': 'Lesson does not exist!'
                }
            )
        except Exception as e:
            logger.error(f"Request:GET Model:Lessons Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'errors': e
                }
            )

    def post(self, request):
        logger.info("Request:POST Model:Lessons")
        if not user_is_instructor(request.user):
            logger.error("Request:POST Model:Lessons Error: PERMISSION DENIED!")
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an instructur to add new lessons"
                }
            )

        serializer = LessonsDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        validated_data = serializer.validated_data

        try:
            if LessonsRepository.lesson_already_exists(validated_data):
                logger.error("Request:POST Model:Lesson Error: Lesson already exists")
                return Response(
                    status=status.HTTP_409_CONFLICT,
                    data={
                        "msg": "Lesson already exists!"
                    }
                )
            lesson = LessonsRepository.create_lesson(request.user, validated_data)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'id': lesson.id,
                }
            )

        except Http404 as e:
            logger.error("Request:POST Model:Lessons Errors: Course does not exist")
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'error': 'Course object not found'
                }
            )

        except Exception as e:
            logger.error(f"Request:POST Model:Lesson Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )

    def put(self, request, pk):
        logger.error(f"Request:PUT Model:Lesson")
        lesson = LessonsRepository.get_lesson_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, lesson):
            logger.error("Request:PUT Model:Lesson Error: PERMISSION DENIED!")
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an authorized instructur to update the lesson"
                }
            )

        try:
            # Update lesson name
            if 'name' in request.data:
                logger.info("Request:PUT Model:Lesson Message:Update lesson name")
                serializer = ValidateLessonName(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data = serializer.validated_data

                if LessonsRepository.lesson_already_exists(validated_data):
                    logger.error("Request:PUT Model:Lesson Error: Lesson already exists")
                    return Response(
                        status=status.HTTP_409_CONFLICT,
                        data={
                            "msg": "Lesson already exists!"
                        }
                    )
                lesson = LessonsRepository.update_lesson_name(lesson, validated_data)

            # Update course active status
            if 'is_active' in request.data:
                logger.info("Request:PUT Model:Lesson Message:Update lesson active status")
                serializer = ValidateLessonActiveStatus(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data = serializer.validated_data

                lesson = LessonsRepository.update_lesson_active_status(lesson, validated_data)

            # Add course subjects
            if 'courses' in request.data:
                logger.info("Request:PUT Model:Lesson Message:Update lesson courses")
                serializer = ValidateLessonCourses(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data = serializer.validated_data

                lesson = LessonsRepository.update_lesson_courses(lesson, validated_data)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'id': lesson.id,
                }
            )
        except Http404 as e:
            logger.error("Request:PUT Model:Lessons Errors: Course does not exist")
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'error': 'Course object not found'
                }
            )
        except Exception as e:
            logger.error(f"Request:PUT Model:Courses Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )

    def delete(self, request, pk):
        logger.info(f"Request:DELETE Model:Lessons")
        lesson = LessonsRepository.get_lesson_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, lesson):
            logger.error("Request:DELETE Model:Lessons Error: PERMISSION DENIED!")
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an authorized instructur to delete the lesson"
                }
            )

        try:
            lesson.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(f"Request:DELETE Model:Lessons Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )
