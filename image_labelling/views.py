from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import FileResponse, HttpResponse

from image_labelling.serializers import (
    MultiImageUploadSerializer,
    ListRequestSerialzier,
    ImageListResponseSerialzier,
    ImageRenderRequestSerializer,
    LabelImageRequestSerializer,
    LabelProcessingRequestSerialzier,
    LabelListRequestSerialzier,
    ImageLabelsListResponseSerialzier,
    ImageSearchRequestSerialzier,
    ImageSearchResponseSerializer,
    LabelByImageIDRequestSerializer,
    LabelsSerializer,
    ImageMetadataSerializer,
)
from image_labelling.utils import (
    ImageHandler,
    ImageAlreadyExists,
    list_images,
    get_image_path,
    ImageDosentExist,
    LabelsManager,
    LabelDoesntExist,
    list_labels,
    LabelSearch,
    get_labels_by_image_id,
    get_image_metadata,
    delete_image,
    UnauthorizedAction,
)


class ImageView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        user = request.user

        images_serialziers = MultiImageUploadSerializer(
            data=dict(request.FILES)
        )
        images_serialziers.is_valid(raise_exception=True)

        errors = list()

        for image in request.FILES.getlist('images'):
            image_handler = ImageHandler(
                image, user
            )
            try:
                image_handler.store()
            except ImageAlreadyExists as e:
                errors.append(e.message)

        if not errors:
            return Response(
                {
                    "message": "Upload succsessful"
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                status=status.HTTP_409_CONFLICT
            )

    def get(self, request):

        serializer = ImageRenderRequestSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        try:
            file_path, content_type = get_image_path(serializer.data["image_id"])
        except ImageDosentExist as e:
    
            return Response(
                {
                    "error": e.message
                }, status=status.HTTP_404_NOT_FOUND
            )

        return FileResponse(
            open(file_path, 'rb'),
            content_type=content_type,
            status=status.HTTP_200_OK
        )

    def delete(self, request):

        user = request.user

        request_serializer = LabelByImageIDRequestSerializer(data=request.GET)
        request_serializer.is_valid(raise_exception=True)

        image_id = request_serializer.data["image_id"]
        try:
            delete_image(user, image_id)
        except UnauthorizedAction as e:
            return Response(
                {
                    "error": e.message
                }, status=status.HTTP_401_Unauthorized
            )

        return Response(
            {
                "message": "Image with id: {} deleted successfully".format(image_id)
            }, status=status.HTTP_200_OK
        )


class ImageListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        data = request.GET

        serialized_request = ListRequestSerialzier(
            data=data
        )
        serialized_request.is_valid(raise_exception=True)

        image_information = list_images(
            serialized_request.data.get("start_idx"), serialized_request.data.get("end_idx"),
            serialized_request.data.get("start_date"), serialized_request.data.get("end_date"),
            status=serialized_request.data.get("status")
        )

        response_serializer = ImageListResponseSerialzier(data=image_information, many=True)
        response_serializer.is_valid()
        
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )


class LabelView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        user = request.user

        request_serialzier = LabelImageRequestSerializer(
            data=request.data, many=True
        )
        request_serialzier.is_valid(raise_exception=True)
        errors = []

        for v in request_serialzier.data:
            image_id = v["image_id"]

            try:
                labels_manager = LabelsManager(user, image_id)
                labels_manager.store(
                    v["coordinates"],
                    v["label"]
                )
            except ImageDosentExist as e:
                errors.append(
                    e.message
                )
        
        return Response(
            {
                "message": "Labels added"
            }, status=status.HTTP_201_CREATED
        ) if not errors else Response(
            {
                "errors": errors
            }, status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request):

        user = request.user

        request_serialzier = LabelProcessingRequestSerialzier(
            data=request.GET
        )
        request_serialzier.is_valid(raise_exception=True)

        label_id = request_serialzier.data["label_id"]
        image_id = request_serialzier.data["image_id"]

        try:
            labels_manager = LabelsManager(user, image_id)
        except ImageDosentExist as e:
            return Response(
                {
                    "error": e.message
                }, status.HTTP_404_NOT_FOUND
            )

        try:
            labels_manager.delete(label_id)
        except LabelDoesntExist as e:
            return Response(
                {
                    "error": e.message
                }, status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "message": "label: {} successfully deleted".format(label_id)
            }, status=status.HTTP_200_OK
        )


    def get(self, request):

        request_serialzier = LabelByImageIDRequestSerializer(
            data=request.GET
        )
        request_serialzier.is_valid(raise_exception=True)

        response_serializer = LabelsSerializer(data=get_labels_by_image_id(request_serialzier.data["image_id"]), many=True)
        response_serializer.is_valid()

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )


class ImageLabelsView(APIView):

    def get(self, request):
        
        request_serialzier = LabelListRequestSerialzier(
            data=request.GET
        )
        request_serialzier.is_valid(raise_exception=True)

        label_information = list_labels(
            request_serialzier.data.get('start_date'), request_serialzier.data.get('end_date'),
            request_serialzier.data.get('status')
        )

        response_serializer = ImageLabelsListResponseSerialzier(data=label_information, many=True)
        response_serializer.is_valid()

        return Response(
            response_serializer.data, status=status.HTTP_200_OK
        )


class ImageLabelsSearchView(APIView):

    def get(self, request):

        request_serialzier = ImageSearchRequestSerialzier(
            data=request.GET
        )
        request_serialzier.is_valid(raise_exception=True)

        label_search = LabelSearch(query=request_serialzier.data["query"])

        response_serializer = ImageSearchResponseSerializer(
            data=label_search.search(), many=True
        )
        response_serializer.is_valid()

        return Response(
            response_serializer.data, status=status.HTTP_200_OK
        )


class ImageMetadataView(APIView):

    def get(self, request):

        request_serialzier = ImageRenderRequestSerializer(
            data=request.GET
        )
        request_serialzier.is_valid(raise_exception=True)

        try:
            metadata = get_image_metadata(
                request_serialzier.data["image_id"]
            )
            response_serializer = ImageMetadataSerializer(
                data=metadata
            )
            response_serializer.is_valid()

            return Response(
                response_serializer.data, status=status.HTTP_200_OK
            )
        except ImageDosentExist as e:

            return Response(
                {
                    "error": e.message
                }, status=status.HTTP_404_NOT_FOUND
            )
