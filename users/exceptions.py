from rest_framework.exceptions import APIException


class PasswordMismatchException(APIException):
    status_code = 400
    default_detail = 'Password Mismatch'
    default_code = 'Password Mismatch'