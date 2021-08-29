import pytest
from django.http import request, response
from image_labelling.tests.utils import (
    IMAGES,
    PASSWORD,
    USER_NAME,
    create_dummy_image_entries,
)
from rest_framework.routers import reverse as router_reverse


@pytest.mark.django_db
class TestImageApi:
    def test_image_list_all_api(self, client):

        create_dummy_image_entries()

        login_path = router_reverse("login")
        response = client.post(
            login_path, data={"username": USER_NAME, "password": PASSWORD}
        )
        path = router_reverse("list_images")
        response = client.get(
            path,
            {"status": "all"},
            HTTP_AUTHORIZATION="JWT {}".format(response.data["access"]),
        )

        assert response.status_code == 200

        for i, v in enumerate(response.data):
            assert v["id"] == str(IMAGES[i]["image_id"])
            assert v["format"] == IMAGES[i]["format"]

    def test_image_list_active_api(self, client):

        create_dummy_image_entries()

        login_path = router_reverse("login")
        response = client.post(
            login_path, data={"username": USER_NAME, "password": PASSWORD}
        )
        path = router_reverse("list_images")
        response = client.get(
            path,
            {"status": "active"},
            HTTP_AUTHORIZATION="JWT {}".format(response.data["access"]),
        )

        active_ids = [str(v["image_id"]) for v in IMAGES if v["status"] == 1]

        assert response.status_code == 200
        assert len(response.data) == len(active_ids)

        for v in response.data:
            assert v["id"] in active_ids

    def test_image_list_inactive_api(self, client):

        create_dummy_image_entries()

        login_path = router_reverse("login")
        response = client.post(
            login_path, data={"username": USER_NAME, "password": PASSWORD}
        )
        path = router_reverse("list_images")
        response = client.get(
            path,
            {"status": "inactive"},
            HTTP_AUTHORIZATION="JWT {}".format(response.data["access"]),
        )

        inactive_ids = [str(v["image_id"]) for v in IMAGES if v["status"] == 0]

        assert response.status_code == 200
        assert len(response.data) == len(inactive_ids)

        for v in response.data:
            assert v["id"] in inactive_ids

    def test_image_delete_api(self, client):

        create_dummy_image_entries()

        login_path = router_reverse("login")
        login_response = client.post(
            login_path, data={"username": USER_NAME, "password": PASSWORD}
        )
        path = router_reverse("image")

        image_to_be_deleted = str(IMAGES[0]["image_id"])

        response = client.delete(
            path + "?image_id={}".format(image_to_be_deleted),
            HTTP_AUTHORIZATION="JWT {}".format(login_response.data["access"]),
        )

        assert response.status_code == 200

        path = router_reverse("list_images")
        response = client.get(
            path,
            {"status": "active"},
            HTTP_AUTHORIZATION="JWT {}".format(login_response.data["access"]),
        )

        for v in response.data:
            assert v["id"] != image_to_be_deleted

    def test_image_metadata_api(self, client):

        create_dummy_image_entries()

        login_path = router_reverse("login")
        login_response = client.post(
            login_path, data={"username": USER_NAME, "password": PASSWORD}
        )
        path = router_reverse("image")

        image_for_which_meta_data_is_fetched = IMAGES[0]

        path = router_reverse("image_metadata")
        response = client.get(
            path,
            {"image_id": str(image_for_which_meta_data_is_fetched["image_id"])},
            HTTP_AUTHORIZATION="JWT {}".format(login_response.data["access"]),
        )

        assert response.status_code == 200
        assert response.data["uploaded_by"] == USER_NAME
        assert response.data["sha"] == image_for_which_meta_data_is_fetched["integrity"]
        assert response.data["format"] == image_for_which_meta_data_is_fetched["format"]
