from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from videos.repository.videos import VideoRepository
from videos.serializers.videos import (
    VideoSerializer, VideoDtoSerializer, ValidateVideoTitle, ValidateVideoLink,
    ValidateVideoActiveStatus, ValidateVideoTags, ValidateVideoLessons)
from users.utils import user_is_instructor, user_is_author


class VideoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        try:
            if pk:
                video = VideoRepository.get_video_by_id(pk)
                serializer = VideoSerializer(video)
            else:
                videos = VideoRepository.get_all_videos()
                serializer = VideoSerializer(videos, many=True)
            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        except Http404 as e:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'errors': 'Video does not exist!'
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
                    'message': "PERMISSION DENIED! You should be an instructur to add new videos"
                }
            )

        serializer = VideoDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        validated_data = serializer.validated_data

        try:
            if VideoRepository.video_already_exists(validated_data):
                return Response(
                    status=status.HTTP_409_CONFLICT,
                    data={
                        "msg": "Video already exists!"
                    }
                )
            video = VideoRepository.create_video(request.user, validated_data)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'id': video.id,
                }
            )
        except Http404 as e:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'error': 'Lesson object not found'
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
        video = VideoRepository.get_video_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, video):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an authorized instructur to delete the video"
                }
            )

        try:
            video.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )
