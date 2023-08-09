from django.urls import path

from .views import *

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('verify_code/', VerifyCode.as_view(), name='verify_code'),
    path('referral/', ReferralAPIView.as_view(), name='referral'),
]
