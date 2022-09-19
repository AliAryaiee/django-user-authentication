from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, exceptions, status

from . import serializers


class UserRegister(APIView):
    """
        User Register Class View
    """

    def post(self, request):
        """
            POST Request
        """
        serialized_user = serializers.UserRegisterSerializer(data=request.data)
        if serialized_user.is_valid(raise_exception=True):
            validated_data = serialized_user.validated_data
            serializers.User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"]
            )
            return Response(serialized_user.data)
