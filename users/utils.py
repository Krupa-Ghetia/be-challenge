from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


def user_is_instructor(user):
    if user.is_instructor:
        return True
    return False


def user_is_author(user, object_to_verify):
    if user.id == object_to_verify.created_by_id:
        return True
    return False
