from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=40)
