from rest_framework import serializers
from common.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'email', 'is_active', 'created_at', 'nickname']


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'new_password']

    @staticmethod
    def get_new_password(obj):
        return obj.password or ''
