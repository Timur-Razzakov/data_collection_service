from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('registration/', registration_view, name='registration'),
    path('verify-code/', verify_code_view, name='verify_code'),
    path('referral/', referralview_view, name='referral'),
]
