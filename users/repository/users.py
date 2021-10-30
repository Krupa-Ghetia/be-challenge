from django.db.models import Q
from django.shortcuts import get_object_or_404

from users.models import User
from users.managers import CustomUserManager


class UserRepository:

    @staticmethod
    def create_user(data):
        user = User.objects.create_user(data['username'], data['email'], data['password'], data['is_instructor'])
        return user

    @staticmethod
    def get_user_object(user_id):
        return get_object_or_404(User, id=user_id)

    @staticmethod
    def user_already_exists(data):
        if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).exists():
            return True
        return False

    @staticmethod
    def update_user_email(user_id, email):
        user = UserRepository.get_user_object(user_id)
        CustomUserManager().update_user_email(user, email)

    @staticmethod
    def update_user_password(user_id, old_password, new_password):
        user = UserRepository.get_user_object(user_id)
        CustomUserManager().update_user_password(user, old_password, new_password)
