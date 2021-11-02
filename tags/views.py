from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
import logging

from tags.repository.tags import TagRepository
from tags.serializers.tags import TagSerializer, ValidateTagName
from users.utils import user_is_instructor, user_is_author

logger = logging.getLogger('be_challenge')


class TagsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        logger.info(f"Request:GET Model:Tags")
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
            logger.error("Request:GET Model:Tags Errors: Tag does not exist")
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'errors': 'Tag does not exist!'
                }
            )
        except Exception as e:
            logger.error(f"Request:GET Model:Tags Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'errors': e
                }
            )

    def post(self, request):
        logger.info("Request:POST Model:Tags")
        if not user_is_instructor(request.user):
            logger.error("Request:POST Model:Tags Error: PERMISSION DENIED!")
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
                logger.error("Request:POST Model:Tags Error: Tag already exists")
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
            logger.error(f"Request:POST Model:Tag Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )

    def put(self, request, pk):
        logger.error(f"Request:PUT Model:Tags")
        tag = TagRepository.get_tag_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, tag):
            logger.error("Request:PUT Model:Tags Error: PERMISSION DENIED!")
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an authorized instructur to update the tag"
                }
            )
        try:
            serializer = ValidateTagName(data=request.data)
            if not serializer.is_valid():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=serializer.errors
                )
            validated_data = serializer.validated_data
            if TagRepository.tag_already_exists(validated_data):
                logger.error("Request:PUT Model:Tag Error: Tag already exists")
                return Response(
                    status=status.HTTP_409_CONFLICT,
                    data={
                        "msg": "Tag already exists!"
                    }
                )
            tag = TagRepository.update_tag_name(tag, validated_data)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'id': tag.id
                }
            )
        except Exception as e:
            logger.error(f"Request:PUT Model:Tag Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'errors': e
                }
            )

    def delete(self, request, pk):
        logger.info(f"Request:DELETE Model:Tags")
        tag = TagRepository.get_tag_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, tag):
            logger.error("Request:DELETE Model:Tags Error: PERMISSION DENIED!")
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
            logger.error(f"Request:DELETE Model:Subject Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )
