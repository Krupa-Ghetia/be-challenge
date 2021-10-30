from rest_framework import serializers
from users.repository.users import UserRepository


class UserDtoSerializer(serializers.Serializer):

    def create(self, validated_data):
        user = UserRepository.create_user(validated_data)
        return user

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    is_instructor = serializers.BooleanField(default=False)
    password = serializers.CharField(max_length=128)


class ValidateEmail(serializers.Serializer):
    email = serializers.EmailField(min_length=4, max_length=254)


class ValidatePassword(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, max_length=128)
    new_password = serializers.CharField(min_length=8, max_length=128)
