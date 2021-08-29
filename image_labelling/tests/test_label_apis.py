from django.http import request, response
from rest_framework.routers import reverse as router_reverse
import pytest

from image_labelling.tests.utils import LABELS, create_dummy_label_entries, IMAGES, USER_NAME, PASSWORD


@pytest.mark.django_db
class TestLabelApi:

    def test_list_image_labels_api(self, client):

        create_dummy_label_entries()

        login_path = router_reverse("login")
        response=client.post(
            login_path, data={
                "username": USER_NAME,
                "password": PASSWORD
            }
        )

        path = router_reverse(
            "label"
        )
        response = client.get(
            path, {'image_id': str(IMAGES[0]["image_id"])},
            HTTP_AUTHORIZATION="JWT {}".format(response.data["access"])
        )

        label_ids_to_consider = [
            str(v["id"])
            for v in LABELS
        ]

        assert response.status_code == 200

        for v in response.data:
            assert v["id"] in label_ids_to_consider

    def test_add_labels(self, client):

        create_dummy_label_entries()

        login_path = router_reverse("login")
        login_response=client.post(
            login_path, data={
                "username": USER_NAME,
                "password": PASSWORD
            }
        )

        path = router_reverse(
            "label"
        )
        image_id = str(IMAGES[0]["image_id"])
        data = [
            {
                "image_id": image_id,
                "coordinates": {
                    "x1": 0.223,
                    "y1": 3.46,
                    "x2": 0.44564,
                    "y2": 6.889
                },
                "label": "stroke"
            }
        ]
        response = client.post(
            path, json=data,
            HTTP_AUTHORIZATION="JWT {}".format(login_response.data["access"])
        )

        assert response.status_code == 201

    def test_delete_label_api(self, client):

        labels = create_dummy_label_entries()

        login_path = router_reverse("login")
        login_response=client.post(
            login_path, data={
                "username": USER_NAME,
                "password": PASSWORD
            }
        )

        path = router_reverse(
            "label"
        )
        response = client.delete(
            path + "?image_id={}&label_id={}".format(str(IMAGES[0]["image_id"]), str(labels[0].id)),
            HTTP_AUTHORIZATION="JWT {}".format(login_response.data["access"])
        )

        assert response.status_code == 200

        path = router_reverse(
            "label"
        )
        response = client.get(
            path, {'image_id': str(IMAGES[0]["image_id"])},
            HTTP_AUTHORIZATION="JWT {}".format(login_response.data["access"])
        )

        for v in response.data:

            assert v["id"] != str(labels[0].id)

    def test_label_search_api(self, client):


        labels = create_dummy_label_entries()

        login_path = router_reverse("login")
        login_response=client.post(
            login_path, data={
                "username": USER_NAME,
                "password": PASSWORD
            }
        )

        path = router_reverse(
            "image_labels_search"
        )
        response = client.get(
            path + "?query={}".format("canc"),
            HTTP_AUTHORIZATION="JWT {}".format(login_response.data["access"])
        )

        assert response.status_code == 200
        assert len(response.data) > 0

        for v in response.data:
            assert v["label"] == "cancer"

    def test_image_label_api(self, client):

        labels = create_dummy_label_entries()

        login_path = router_reverse("login")
        login_response=client.post(
            login_path, data={
                "username": USER_NAME,
                "password": PASSWORD
            }
        )

        path = router_reverse(
            "image_labels_list"
        )
        response = client.get(
            path, {'status': "all"},
            HTTP_AUTHORIZATION="JWT {}".format(login_response.data["access"])
        )

        assert response.status_code == 200

        assert len(response.data) > 0
