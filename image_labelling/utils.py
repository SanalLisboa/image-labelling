import codecs
import datetime
import hashlib
import uuid
from io import BytesIO
from typing import Any, Dict, List, Tuple

import textdistance
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q

from image_labelling.exceptions import (
    ImageAlreadyExists,
    ImageDosentExist,
    LabelDoesntExist,
    UnauthorizedAction,
)
from image_labelling.models import Image, Label
from image_labelling.settings import TEMP_FILE_STORAGE_PATH, StatusMapper


class ImageHandler:
    """The image handler class is responsible for storing file to filesystem
    and creating a db entry for the same"""

    def __init__(self, file: InMemoryUploadedFile, user: User) -> None:

        self._filename: str = file.name
        self._format: str = file.name.split(".")[-1]
        self._bytes_obj: BytesIO = file.read()
        self._sha: str = hashlib.sha256(self._bytes_obj).hexdigest()
        self._uuid: uuid.uuid4 = uuid.uuid4()
        self._user: User = user

    def _write_image_fs(self) -> None:
        """Wirtes image file in form of bytes to file system."""

        with open(
            "{}/{}.{}".format(TEMP_FILE_STORAGE_PATH, str(self._uuid), self._format),
            "wb+",
        ) as f:
            f.write(self._bytes_obj)

    def _verify_image_object_present(self) -> bool:
        """This method verifies if a image is present in the database or not."""

        try:
            image = Image.objects.get(integrity=self._sha)
            if image.status == 0:
                return False
            return True
        except Image.DoesNotExist:
            return False

    def _create_db_object(self):
        """Creates a image data entry in the database."""

        Image.objects.create(
            id=self._uuid, format=self._format, integrity=self._sha, user=self._user
        )

    def _check_inactive(self) -> bool:
        """This method checks if an image is marked as inactive or not."""

        try:
            image = Image.objects.get(integrity=self._sha)
            if image.status == 0:
                return True
        except Image.DoesNotExist:
            return False

    def store(self):
        """The main method responible to store a image in filesystem and database."""

        if self._verify_image_object_present():

            raise ImageAlreadyExists(
                "Image with name {} already exists and has a matching hash({}) with other image in database.".format(
                    self._filename, self._sha
                )
            )

        if self._check_inactive():
            image = Image.objects.get(integrity=self._sha)
            image.status = 1
            image.save()
        else:
            self._write_image_fs()
            self._create_db_object()


def delete_image(user: User, image_id: str) -> None:
    """This function is responsibe for deleting image ie deactiving the image from database."""
    try:
        image = Image.objects.get(id=image_id)

        if user != image.user:
            raise UnauthorizedAction(
                "Not permitted to delete image uploaded by user: {}".format(
                    user.username
                )
            )

        image.status = 0
        image.save()
        query_set = Label.objects.filter(image_id=image_id)

        for v in query_set:
            v.status = 0
            v.save()

    except Image.DoesNotExist:
        pass


def list_images(
    start_idx: int,
    end_idx: int,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    status: str,
) -> List[Dict[str, str]]:
    """This function is responsible for listing all images in given index range or given date range"""

    status = getattr(StatusMapper, status).value

    if not start_date and not end_date:
        if status is None:
            image_queryset = Image.objects.all().order_by("uploaded_on")
        else:
            image_queryset = Image.objects.filter(status=status).order_by("uploaded_on")
    else:
        if status is None:
            image_queryset = Image.objects.filter(
                uploaded_on__range=[start_date, end_date]
            )
        else:
            image_queryset = Image.objects.filter(
                uploaded_on__range=[start_date, end_date], status=status
            )

    if ((start_idx or start_idx == 0) and (end_idx or end_idx == 0)) and (
        not start_date and not end_date
    ):

        image_queryset = image_queryset[start_idx:end_idx]

    image_information = list()

    for image_obj in image_queryset:

        image_information.append(
            {
                "created_by": image_obj.user.username,
                "id": image_obj.id,
                "uploaded_on": image_obj.uploaded_on,
                "format": image_obj.format,
            }
        )

    return image_information


def get_image_obj(image_id: str) -> bool:
    """This function returns and image orm object given image id."""

    try:
        image = Image.objects.get(id=image_id)
        if image.status == 0:
            return None
        return image
    except Image.DoesNotExist:
        return None


def get_image_path(image_id) -> Tuple[str, str]:
    """This function returns image path for where the image is stored in file system."""

    image = get_image_obj(image_id)

    if not image:
        raise ImageDosentExist("Image with id {} doesn't exist".format(image_id))

    file_path = "{}/{}.{}".format(TEMP_FILE_STORAGE_PATH, str(image.id), image.format)
    content_type = "image/{}".format(image.format)

    return file_path, content_type


class LabelsManager:
    """This class is responsible for management of labels"""

    def __init__(self, user: User, image_id: uuid.uuid4) -> None:

        self._image = get_image_obj(image_id)

        if not self._image or self._image.status == 0:
            raise ImageDosentExist("Image with id {} doesn't exist".format(image_id))

        self._user = user
        self._image_id = image_id

    def _get_queryset_if_label_exists(self, label_value: str) -> Label:
        """ "Returns a label object register by the user for an image with give label value"""

        try:
            label = Label.objects.get(
                user_id=self._user.id, image_id=self._image_id, label=label_value
            )
            return label
        except Label.DoesNotExist:
            return None

    def _update_existing_label(self, label_obj, coordinates: Dict[str, float]) -> None:
        """This method updates the existing label or cordinates of it."""

        x1 = coordinates["x1"]
        x2 = coordinates["x2"]
        y1 = coordinates["y1"]
        y2 = coordinates["y2"]

        if (
            label_obj.x1 != x1
            or label_obj.x2 != x2
            or label_obj.y1 != y1
            or label_obj.y2 != y2
        ):
            label_obj.x1 = x1
            label_obj.x2 = x2
            label_obj.y1 = y1
            label_obj.y2 = y2

            label_obj.save()
        elif label_obj.status == 0:
            label_obj.status = 1

            label_obj.save()

    def _insert_new_label(
        self, coordinates: Dict[str, float], label_value: str
    ) -> None:
        """This function inserts a new label for an image."""

        id = uuid.uuid4()
        x1 = coordinates["x1"]
        x2 = coordinates["x2"]
        y1 = coordinates["y1"]
        y2 = coordinates["y2"]

        label = Label.objects.create(
            id=id,
            image_id=self._image,
            user_id=self._user,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            label=label_value,
        )

    def store(self, coordinates: Dict[str, float], label: str) -> None:
        """This method is responsible to perform all computations requried for storing labels."""

        label_obj = self._get_queryset_if_label_exists(label)

        if label_obj:
            self._update_existing_label(label_obj, coordinates)
        else:
            self._insert_new_label(coordinates, label)

    def delete(self, label_id: str) -> None:
        """ "This method is responsible for deactiving active labels."""

        try:
            label_obj = Label.objects.get(
                user_id=self._user.id,
                image_id=self._image_id,
                id=label_id,
            )
            label_obj.status = 0
            label_obj.save()
            return None
        except Label.DoesNotExist:
            raise LabelDoesntExist(
                "label: {} doesn't exists for user: {}".format(
                    label_id, self._user.username
                )
            )


def list_labels(start_date, end_date, status) -> List[Dict[str, str]]:
    """This function is responsible for listing labels in given date range."""

    status = getattr(StatusMapper, status).value

    if start_date and end_date:
        if status is None:
            label_queryset = Label.objects.filter(
                updated_at__range=[start_date, end_date]
            )
        else:
            label_queryset = Label.objects.filter(
                updated_at__range=[start_date, end_date], status=status
            )
    else:
        if status is None:
            label_queryset = Label.objects.all().order_by("updated_at")
        else:
            label_queryset = Label.objects.filter(status=status).order_by("updated_at")

    label_information = dict()

    for label_obj in label_queryset:

        dict_key = (
            label_obj.image_id.id,
            label_obj.image_id.format,
            label_obj.image_id.uploaded_on,
            label_obj.image_id.user.username,
            label_obj.image_id.status,
        )

        if dict_key not in label_information:
            label_information[dict_key] = []

        label_information[dict_key].append(
            {
                "created_by": label_obj.user_id.username,
                "id": label_obj.id,
                "created_at": label_obj.created_at,
                "updated_at": label_obj.updated_at,
                "label": label_obj.label,
                "coordinates": {
                    "x1": label_obj.x1,
                    "x2": label_obj.x2,
                    "y1": label_obj.y1,
                    "y2": label_obj.y2,
                },
            }
        )

    return [
        {
            "image_id": k[0],
            "image_format": k[1],
            "image_uploaded_on": k[2],
            "image_created_by": k[3],
            "labels": v,
            "image_status": k[4],
        }
        for k, v in label_information.items()
    ]


class LabelSearch:
    """This class is responsible for performing label search given a query parm."""

    @staticmethod
    def text_distance(t1: str, t2: str) -> float:
        """This method is responsible for computing jaccard similarity between two strings"""

        return textdistance.jaccard.normalized_similarity(t1.lower(), t2.lower())

    def __init__(self, query: str) -> None:

        self._query = query

    def _query_set_contains(self):
        """Returns queryset after performing icontains"""

        return Label.objects.filter(label__icontains=self._query, status=1)

    def _query_set_search(self):
        """Returns querysert after performing serach for given query."""

        return Label.objects.filter(label__search=self._query, status=1)

    def search(self) -> Dict[str, Any]:
        """Method that computes search and returns the search result."""

        query_set = list(self._query_set_contains()) + list(self._query_set_search())

        search_list = set(
            [(v, LabelSearch.text_distance(self._query, v.label)) for v in query_set]
        )
        search_list = sorted(search_list, key=lambda x: x[1], reverse=True)

        return [
            {
                "image_id": v.image_id.id,
                "image_format": v.image_id.format,
                "image_uploaded_on": v.image_id.uploaded_on,
                "image_uploaded_by": v.image_id.user.username,
                "label_id": v.id,
                "label_created_at": v.created_at,
                "label_updated_at": v.updated_at,
                "labeled_by": v.user_id.username,
                "label": v.label,
                "coordinates": {
                    "x1": v.x1,
                    "y1": v.y1,
                    "x2": v.x2,
                    "y2": v.y2,
                },
                "similarity": similarity,
            }
            for v, similarity in search_list
            if (similarity > 0.5 and v.status == 1)
        ]


def get_labels_by_image_id(image_id: uuid.uuid4) -> Dict[str, Any]:
    """This function is responsible for getting labels given image id"""

    query_set = Label.objects.filter(image_id=image_id, status=1).order_by("updated_at")

    return [
        {
            "created_by": v.user_id.username,
            "id": v.id,
            "created_at": v.created_at,
            "updated_at": v.updated_at,
            "label": v.label,
            "coordinates": {"x1": v.x1, "y1": v.y1, "x2": v.x2, "y2": v.y2},
        }
        for v in query_set
    ]


def get_image_metadata(image_id: uuid.uuid4) -> Dict[str, Any]:
    """This function is responsible for retriving image metadata given image id."""

    try:
        image = Image.objects.get(id=image_id)
        if image.status == 0:
            ImageDosentExist("Image with id: {} doesn't exist.".format(image_id))
        return {
            "uploaded_by": image.user.username,
            "uploaded_on": image.uploaded_on,
            "sha": image.integrity,
            "format": image.format,
        }
    except Image.DoesNotExist:
        raise ImageDosentExist("Image with id: {} doesn't exist.".format(image_id))
