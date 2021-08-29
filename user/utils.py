from typing import Dict

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserExistException(Exception):
    
    def __init__(self, message: str):

        self.message = message
        super().__init__(message)


def create_user(data: Dict[str, str]) -> User:

    try:

        User.objects.get(
            username=data['username']
        )
        raise UserExistException(
            "User with username {}, already exists".format(data['username'])
        )

    except User.DoesNotExist:

        user = User.objects.create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            username=data['username'],
            password=data['password'],
        )

    return user
