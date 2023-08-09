from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('verify-code/', VerifyCode.as_view(), name='verify_code'),
    path('referral/', ReferralAPIView.as_view(), name='referral'),
]
