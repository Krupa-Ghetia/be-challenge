from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers.users import UserDtoSerializer
from users.utils import get_token_for_user


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
            print(e)
