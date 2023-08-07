from rest_framework import serializers

from models import UserProfile, InviteCode


class UserProfileSerializer(serializers.ModelSerializer):
    """для профиля пользователя"""

    class Meta:
        model = UserProfile
        fields = '__all__'


class PhoneNumberSerializer(serializers.Serializer):
    """для отправки сообщений"""
    phone_number = serializers.CharField(max_length=15)


class VerificationCodeSerializer(serializers.Serializer):
    """для верификации кода """
    code = serializers.CharField(max_length=4)


class InviteCodeSerializer(serializers.Serializer):
    """для ввода и активации инвайт-кода """
    code = serializers.CharField(max_length=6)
