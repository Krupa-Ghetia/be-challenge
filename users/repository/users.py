from users.models import User


class UserRepository:

    @staticmethod
    def create_user(data):
        user = User.objects.create_user(data['username'], data['email'], data['password'], data['is_instructor'])
        return user

