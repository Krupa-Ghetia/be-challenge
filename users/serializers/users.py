from rest_framework import serializers
from users.models import User
from users.repository.users import UserRepository


class UserDtoSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        user = UserRepository.create_user(validated_data)
        return user

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    is_instructor = serializers.BooleanField(default=False)
    password = serializers.CharField(max_length=128)