from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
import logging

from subjects.repository.subjects import SubjectsRepository
from subjects.serializers.subjects import SubjectsSerializer, ValidateSubjectName
from users.utils import user_is_instructor, user_is_author

logger = logging.getLogger('be_challenge')


class SubjectsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        logger.info(f"Request:GET Model:Subjects")
        try:
            if pk:
                subject = SubjectsRepository.get_subject_by_id(pk)
                serializer = SubjectsSerializer(subject)
            else:
                subjects = SubjectsRepository.get_all_subjects()
                serializer = SubjectsSerializer(subjects, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'subjects': serializer.data
                }
            )

        except Http404 as e:
            logger.error("Request:GET Model:Subjects Errors: Subject does not exist")
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'errors': 'Subject does not exist!'
                }
            )
        except Exception as e:
            logger.error(f"Request:GET Model:Subject Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'errors': e
                }
            )

    def post(self, request):
        logger.info("Request:POST Model:Subjects")
        if not user_is_instructor(request.user):
            logger.error("Request:POST Model:Subjects Error: PERMISSION DENIED!")
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an instructur to add new Subjects"
                }
            )

        serializer = ValidateSubjectName(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        validated_data = serializer.validated_data

        try:
            if SubjectsRepository.subject_already_exists(validated_data):
                logger.error("Request:POST Model:Subjects Error: Subject already exists")
                return Response(
                    status=status.HTTP_409_CONFLICT,
                    data={
                        "msg": "Subject already exists!"
                    }
                )
            subject = SubjectsRepository.create_subject(request.user, validated_data)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'id': subject.id,
                }
            )

        except Exception as e:
            logger.error(f"Request:POST Model:Subject Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )

    def put(self, request, pk=None):
        logger.error(f"Request:PUT Model:Subject")
        subject = SubjectsRepository.get_subject_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, subject):
            logger.error("Request:PUT Model:Subject Error: PERMISSION DENIED!")
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an authorized instructur to update the subject"
                }
            )

        serializer = ValidateSubjectName(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        validated_data = serializer.validated_data

        try:
            if SubjectsRepository.subject_already_exists(validated_data):
                logger.error("Request:PUT Model:Subject Error: Subject already exists")
                return Response(
                    status=status.HTTP_409_CONFLICT,
                    data={
                        "msg": "Subject already exists!"
                    }
                )
            subject = SubjectsRepository.update_subject(subject, validated_data)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'id': subject.id
                }
            )

        except Exception as e:
            logger.error(f"Request:PUT Model:Subject Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )

    def delete(self, request, pk=None):
        logger.info(f"Request:DELETE Model:Subject")
        subject = SubjectsRepository.get_subject_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, subject):
            logger.error("Request:DELETE Model:Subject Error: PERMISSION DENIED!")
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an authorized instructur to delete the subject"
                }
            )
        try:
            subject.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(f"Request:DELETE Model:Subject Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )
