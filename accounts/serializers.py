from rest_framework import serializers

from accounts.models import User, Referral

from .utils import random_string_generator


class UserProfileSerializer(serializers.ModelSerializer):
    """для профиля пользователя"""
    my_referrals = serializers.SerializerMethodField('get_users')
    my_referer = serializers.SerializerMethodField('get_invite_code')

    class Meta:
        model = User
        fields = (
            "phone_number",
            "invite_code",
            "my_referrals",  # пользователи, которые использовали мой invite_code
            "my_referer"  # invite_code, который я использовал
        )

    def get_users(self, obj):
        get_user_referrals = Referral.objects.filter(referral=obj).values_list('user', flat=True)
        return User.objects.filter(id__in=get_user_referrals).values_list('phone_number', flat=True)

    def get_invite_code(self, obj):
        get_user_referer = Referral.objects.filter(user=obj).first()
        return get_user_referer.referral.invite_code


class VerificationCodeSerializer(serializers.Serializer):
    """для верификации кода """
    activate_code = serializers.CharField(max_length=4, default=None)
    phone_number = serializers.CharField(max_length=11, )


class ReferralSerializers(serializers.ModelSerializer):
    invite_code = serializers.CharField(max_length=6, default=None, write_only=True)

    class Meta:
        model = Referral
        fields = ('user', 'referral', 'invite_code')
        read_only_fields = ['user', 'referral']
