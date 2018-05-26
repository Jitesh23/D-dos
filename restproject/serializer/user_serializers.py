from rest_framework import serializers
from users.models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class TokenAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()