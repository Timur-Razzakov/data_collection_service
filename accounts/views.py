from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User, Referral
from frontend.forms import UserLoginForm
from .serializers import VerificationCodeSerializer, UserProfileSerializer, ReferralSerializers
from .utils import random_string_generator, send_message


# from .models import UserProfile, InviteCode
# from .utils import random_string_generator, wait


#


class RegistrationView(APIView):
    """Получаем код активации и сохраняем в бд"""
    def post(self, request):
        phone_serializer = VerificationCodeSerializer(data=request.data)
        if phone_serializer.is_valid():
            # Создаем или получаем профиль пользователя по номеру телефона
            phone_number = phone_serializer.validated_data['phone_number']
            activate_code = random_string_generator(size=4)
            user_profile = User.objects.filter(phone_number=phone_number).first()
            if not user_profile:
                user_profile = User.objects.create_user(phone_number=phone_number)
            # Связываем код активации с профилем пользователя
            user_profile.activate_code = activate_code
            user_profile.save()
            # Имитация отправки кода авторизации (1-2 сек задержка)
            send_message()
            return Response({"auth_code": activate_code},
                            status=status.HTTP_200_OK)
        return Response(phone_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCode(APIView):
    """Проверяем введенный код активации и связываем с профилем пользователя"""

    def post(self, request):
        verification_serializer = VerificationCodeSerializer(data=request.data)
        if verification_serializer.is_valid():
            phone_number = verification_serializer.validated_data['phone_number']
            verification_code = verification_serializer.validated_data['activate_code']
            try:
                user_profile = User.objects.get(phone_number=phone_number,
                                                activate_code=verification_code)
                user_profile.is_active = True
                user_profile.save()
                return Response({"detail": "Verification successful."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"detail": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(verification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferralAPIView(APIView):
    """Проверяем """

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer_class = UserProfileSerializer(instance=user)
        return Response(serializer_class.data,
                        status=status.HTTP_200_OK)

    def post(self, request):
        # получаем invite_code, который хотим использовать как реферальный
        referral_serializer = ReferralSerializers(data=request.data)
        referral_serializer.is_valid(raise_exception=True)
        invite_code = referral_serializer.validated_data['invite_code']

        # пользователь, который хочет записать себе invite_code
        user = request.user

        check_invite = Referral.objects.filter(user=user.pk).first()
        if check_invite:
            return Response({"detail": "Вы уже активировали 'invite_code' "},
                            status=status.HTTP_400_BAD_REQUEST)
        # ищем владельца invite_code-да
        referral_user = get_object_or_404(User, invite_code=invite_code)
        if referral_user.pk == user.pk:
            return Response({"detail": "Вы не можете активировать свой 'invite_code' "},
                            status=status.HTTP_400_BAD_REQUEST)

        referral = Referral.objects.create(user=user, referral=referral_user)
        referral.save()
        # referral_serializer.instance = referral
        # return Response(referral_serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Save successful."}, status=status.HTTP_200_OK)
