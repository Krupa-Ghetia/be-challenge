from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from subjects.repository.subjects import SubjectsRepository
from subjects.serializers.subjects import SubjectsSerializer, ValidateSubjectName
from users.utils import user_is_instructor, user_is_author


class SubjectsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
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
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'errors': 'Lesson does not exist!'
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
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )

    def put(self, request, pk=None):
        subject = SubjectsRepository.get_subject_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, subject):
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
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )

    def delete(self, request, pk=None):
        subject = SubjectsRepository.get_subject_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, subject):
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
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )
