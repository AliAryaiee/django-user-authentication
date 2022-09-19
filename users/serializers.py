from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
        User Register Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = User
        fields = "__all__"
        exclude = []
        extra_kwargs = {
            "password": {"write_only": True}
        }
