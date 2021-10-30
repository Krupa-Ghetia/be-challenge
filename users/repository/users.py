from django.db.models import Q
from users.models import User


class UserRepository:

    @staticmethod
    def create_user(data):
        user = User.objects.create_user(data['username'], data['email'], data['password'], data['is_instructor'])
        return user

    @staticmethod
    def user_already_exists(data):
        if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).exists():
            return True
