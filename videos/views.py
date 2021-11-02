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

    def get(self, request, lesson=None, pk=None):
        try:
            if pk:
                video = VideoRepository.get_video_by_id(pk)
                video = VideoRepository.update_video_view_count(video)
                serializer = VideoSerializer(video)
            elif lesson:
                videos = VideoRepository.get_videos_by_lesson(lesson, request.user, request.query_params)
                serializer = VideoSerializer(videos, many=True)
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
        video = VideoRepository.get_video_by_id(pk)
        if not user_is_instructor(request.user) or not user_is_author(request.user, video):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': "PERMISSION DENIED! You should be an authorized instructur to update the video"
                }
            )
        try:
            # Update video title
            if 'title' in request.data:
                serializer = ValidateVideoTitle(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data = serializer.validated_data
                if VideoRepository.video_already_exists(validated_data):
                    return Response(
                        status=status.HTTP_409_CONFLICT,
                        data={
                            "msg": "Video already exists!"
                        }
                    )
                video = VideoRepository.update_video_title(video, validated_data)

            # Update video link
            if 'link' in request.data:
                serializer = ValidateVideoLink(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data=serializer.validated_data
                video = VideoRepository.update_video_link(video, validated_data)

            # Update video active status
            if 'is_active' in request.data:
                serializer = ValidateVideoActiveStatus(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data = serializer.validated_data
                video = VideoRepository.update_video_active_status(video, validated_data)

            # Update video tags
            if 'tags' in request.data:
                serializer = ValidateVideoTags(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data = serializer.validated_data
                video = VideoRepository.update_video_tags(video, validated_data, request.user)

            # Update video lessons
            if 'lessons' in request.data:
                serializer = ValidateVideoLessons(data=request.data)
                if not serializer.is_valid():
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors
                    )
                validated_data = serializer.validated_data
                video = VideoRepository.update_video_lessons(video, validated_data)

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


class VideoAnalyticsView(APIView):
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
            videos = VideoRepository.get_most_viewed_videos()
            serializer = VideoSerializer(videos, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'errors': e
                }
            )
