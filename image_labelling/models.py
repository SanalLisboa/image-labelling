import uuid

from django.contrib.auth.models import User
from django.db import models

from image_labelling.settings import IMAGE_FORMAT_TYPES


class Image(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    format = models.CharField(max_length=10, choices=IMAGE_FORMAT_TYPES)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    integrity = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "id",
                    "integrity",
                ]
            ),
        ]
        unique_together = [("integrity",)]


class Label(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    x1 = models.FloatField()
    y1 = models.FloatField()
    x2 = models.FloatField()
    y2 = models.FloatField()
    label = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["id", "user_id", "image_id", "label"])]
        unique_together = (("user_id", "image_id", "label"),)
