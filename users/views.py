from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
import logging

from users.serializers.users import UserDtoSerializer, ValidateEmail, ValidatePassword
from users.utils import get_token_for_user
from users.repository.users import UserRepository
from users.exceptions import PasswordMismatchException

logger = logging.getLogger('be_challenge')


class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        logger.info("Request:POST Model:Users")
        serializer = UserDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'error': serializer.errors
                }
            )

        validated_data = serializer.validated_data

        try:
            if UserRepository.user_already_exists(validated_data):
                logger.error("Request:POST Model:Users Error:Username or email already exists!")
                return Response(
                    status=status.HTTP_409_CONFLICT,
                    data={
                        "msg": "Username or email already exists!"
                    }
                )

            user = serializer.create(validated_data)
            tokens = get_token_for_user(user)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'access_token': tokens.get('access'),
                    'refresh_token': tokens.get('refresh')
                }
            )

        except Exception as e:
            logger.error(f"Request:POST Model:Users Error: {e}")
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    'error': e
                }
            )


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        logger.error(f"Request:PUT Model:Users")

        user = request.user
        # Update user email
        if 'email' in request.data:
            logger.info("Request:PUT Model:Users Message:Update user email")
            serializer = ValidateEmail(data=request.data)
            if not serializer.is_valid():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'error': serializer.errors
                    }
                )

            validated_data = serializer.validated_data

            try:
                user = UserRepository.update_user_email(user.id, validated_data['email'])
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "id": user.id
                    }
                )

            except Exception as e:
                logger.error(f"Request:PUT Model:Users Error: {e}")
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data={
                        'error': e
                    }
                )

        # Update user password
        if 'old_password' in request.data and 'new_password' in request.data:
            logger.info("Request:PUT Model:Users Message:Update user password")
            serializer = ValidatePassword(data=request.data)
            if not serializer.is_valid():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'error': serializer.errors
                    }
                )

            validated_data = serializer.validated_data

            try:
                user = UserRepository.update_user_password(user.id, validated_data['old_password'],
                                                           validated_data['new_password'])
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "id": user.id
                    }
                )

            except PasswordMismatchException as e:
                logger.error(f"Request:PUT Model:Users Error: Password mismatch")
                return Response(
                    status=e.status_code,
                    data={
                        'error': e.default_detail
                    }
                )

            except Exception as e:
                logger.error(f"Request:PUT Model:Users Error: {e}")
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data={
                        'error': e
                    }
                )

        if 'old_password' not in request.data:
            logger.error(f"Request:PUT Model:Users Error: Old password is required")
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'error': 'Old password is required'
                }
            )

        if 'new_password' not in request.data:
            logger.error(f"Request:PUT Model:Users Error: New password is required")
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'error': 'New password is required'
                }
            )
