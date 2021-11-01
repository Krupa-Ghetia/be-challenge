from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from tags.repository.tags import TagRepository
from tags.serializers.tags import TagSerializer, ValidateTagName
from users.utils import user_is_instructor, user_is_author


class TagsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        try:
            if pk:
                tag = TagRepository.get_tag_by_id(pk)
                serializer = TagSerializer(tag)
            else:
                tags = TagRepository.get_all_tags()
                serializer = TagSerializer(tags, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        except Http404 as e:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'errors': 'Tag does not exist!'
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
                    'message': "PERMISSION DENIED! You should be an instructur to add new tags"
                }
            )
        serializer = ValidateTagName(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        validated_data = serializer.validated_data

        try:
            if TagRepository.tag_already_exists(validated_data):
                return Response(
                    status=status.HTTP_409_CONFLICT,
                    data={
                        "msg": "Tag already exists!"
                    }
                )
            tag = TagRepository.create_tag(request.user, validated_data)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'id': tag.id,
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
        pass

    def delete(self, request, pk):
        tag = TagRepository.get_tag_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, tag):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an authorized instructur to delete the tag"
                }
            )
        try:
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )
