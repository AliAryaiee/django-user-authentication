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


class UserProfile(APIView):
    """
        Retrieve User Class View
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_user_object(self, username: str):
        """
            Find User by Username
        """
        try:
            return serializers.User.objects.get(username=username)
        except serializers.User.DoesNotExist:
            return None

    def get(self, request, username: str):
        """
            GET Request
        """
        db_user = self.get_user_object(username=username)
        if db_user:
            serialized_data = serializers.UserRegisterSerializer(
                instance=db_user
            )
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        Response(
            {"response": f"There Is Not User by Username ({username})"},
            status=status.HTTP_400_BAD_REQUEST
        )
