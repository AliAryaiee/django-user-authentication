import jwt
import datetime
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, exceptions, status

from . import serializers
from App.settings import SIMPLE_JWT, SECRET_KEY


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

    def get_user_object(self, user_id: int):
        """
            Find User by Username
        """
        try:
            return serializers.User.objects.get(id=user_id)
        except serializers.User.DoesNotExist:
            return None

    def get(self, request):
        """
            GET Request
        """
        JWT = request.headers["Authorization"].split(" ")[-1]
        if not JWT:
            raise exceptions.AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(
                JWT, SIMPLE_JWT.get("SIGNING_KEY"),
                algorithms=["HS256"]
            )
            db_user = self.get_user_object(user_id=int(payload["user_id"]))
            if db_user:
                serialized_data = serializers.UserRegisterSerializer(
                    instance=db_user
                )
                return Response(serialized_data.data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Unauthenticated!")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid Token")
        return Response(
            {"response": "Unauthenticated"},
            status=status.HTTP_401_UNAUTHORIZED
        )
