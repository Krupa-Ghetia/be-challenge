from django.contrib.auth.base_user import BaseUserManager
from users.exceptions import PasswordMismatchException
from datetime import datetime


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password, is_instructor, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_instructor=is_instructor, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def update_user_email(self, user, email):
        user.email = self.normalize_email(email)
        user.row_last_updated = datetime.now()
        user.save()
        return user

    def update_user_password(self, user, old_password, new_password):
        if not user.check_password(old_password):
            raise PasswordMismatchException('Password Mismatch')
        user.set_password(new_password)
        user.row_last_updated = datetime.now()
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, is_instructor=True, **extra_fields)
