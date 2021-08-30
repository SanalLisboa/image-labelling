from typing import Dict

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from user.exceptions import UserExistException


def create_user(data: Dict[str, str]) -> User:
    """This function is used to create a user."""

    try:

        User.objects.get(username=data["username"])
        raise UserExistException(
            "User with username {}, already exists".format(data["username"])
        )

    except User.DoesNotExist:

        user = User.objects.create_user(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            username=data["username"],
            password=data["password"],
        )

    return user
