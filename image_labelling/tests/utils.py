import datetime
import hashlib
import random
import uuid

from image_labelling.models import Image, Label, User
from user.utils import create_user

IMAGES = [
    {
        "image_id": uuid.uuid4(),
        "format": "png",
        "uploaded_on": datetime.datetime.now(),
        "integrity": hashlib.sha256(
            str(random.randint(0, 100000)).encode()
        ).hexdigest(),
        "status": 1,
    },
    {
        "image_id": uuid.uuid4(),
        "format": "png",
        "uploaded_on": datetime.datetime.now(),
        "integrity": hashlib.sha256(
            str(random.randint(0, 100000)).encode()
        ).hexdigest(),
        "status": 1,
    },
    {
        "image_id": uuid.uuid4(),
        "format": "png",
        "uploaded_on": datetime.datetime.now(),
        "integrity": hashlib.sha256(
            str(random.randint(0, 100000)).encode()
        ).hexdigest(),
        "status": 0,
    },
    {
        "image_id": uuid.uuid4(),
        "format": "png",
        "uploaded_on": datetime.datetime.now(),
        "integrity": hashlib.sha256(
            str(random.randint(0, 100000)).encode()
        ).hexdigest(),
        "status": 1,
    },
]

LABELS = [
    {
        "id": uuid.uuid4(),
        "status": 1,
        "x1": 0.343,
        "y1": 0.456,
        "x2": 0.456,
        "y2": 0.556,
        "label": "cancer",
    },
    {
        "id": uuid.uuid4(),
        "status": 0,
        "x1": 0.343,
        "y1": 0.456,
        "x2": 0.456,
        "y2": 0.556,
        "label": "asthma",
    },
    {
        "id": uuid.uuid4(),
        "status": 1,
        "x1": 0.343,
        "y1": 0.456,
        "x2": 0.456,
        "y2": 0.556,
        "label": "copd",
    },
]

USER_NAME = "ApiTest"
PASSWORD = "temp+password"


def create_dummy_user():

    user = create_user(
        {
            "first_name": "test",
            "last_name": "test",
            "username": USER_NAME,
            "email": "ImageApiTest@admin.com",
            "password": PASSWORD,
        }
    )

    return user


def create_dummy_image_entries():

    user = create_dummy_user()

    images = []

    for image in IMAGES:

        images.append(
            Image.objects.create(
                id=image["image_id"],
                format=image["format"],
                uploaded_on=image["uploaded_on"],
                integrity=image["integrity"],
                status=image["status"],
                user=user,
            )
        )

    return user, images


def create_dummy_label_entries():

    user, images = create_dummy_image_entries()
    labels = []

    for v in LABELS:

        labels.append(
            Label.objects.create(
                id=v["id"],
                image_id=images[0],
                user_id=user,
                status=v["status"],
                x1=v["x1"],
                x2=v["x2"],
                y1=v["y1"],
                y2=v["y2"],
                label=v["label"],
            )
        )

    return labels
