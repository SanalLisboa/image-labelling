from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.serializers import RegisterSerializer
from user.utils import create_user, UserExistException


class RegisterView(APIView):

    def post(self, request):

        request_serializer = RegisterSerializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)

        try:
            user = create_user(request_serializer.data)
        except UserExistException as e:
            return Response(
                {
                    "error": e.message
                }, status=status.HTTP_409_CONFLICT
            )

        return Response(
            {
                "message": "Registeration successfull"
            }, status=status.HTTP_201_CREATED
        )
 