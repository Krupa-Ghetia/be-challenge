from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.serializers.users import UserDtoSerializer
from users.utils import get_token_for_user
from users.repository.users import UserRepository


class UserRegistrationView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):

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
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
