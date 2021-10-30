from django.contrib.auth import get_user_model
import pytest


class TestUsersManager:

    @pytest.mark.django_db
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='regular', email='regular@user.com',
                                        password='regular123', is_instructor=True)

        assert user.username == 'regular'
        assert user.email == 'regular@user.com'
        assert user.is_instructor is True
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    @pytest.mark.django_db
    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(username='super', email='super@user.com',
                                             password='super123')

        assert user.username == 'super'
        assert user.email == 'super@user.com'
        assert user.is_instructor is True
        assert user.is_active is True
        assert user.is_staff is True
        assert user.is_superuser is True
