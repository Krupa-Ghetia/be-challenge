from django.core.exceptions import PermissionDenied
from users.repository.users import UserRepository


def user_is_instructor(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        user_obj = UserRepository.get_user_object(user.id)
        if user_obj.is_instructor:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
