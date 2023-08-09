import os
import requests
from django.shortcuts import render, redirect

from frontend.forms import UserLoginForm, InviteCodeForm

# api_url = os.environ.get('API_URL')
# print(api_url)
API_URL = "http://127.0.0.1:8800/api/"


def home_view(request):
    """Домашняя страница"""
    return render(request, 'home.html', )


def registration_view(request):
    """Функция для регистрации"""
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        response = requests.post(
            url=f"{API_URL}registration/",
            data=data)
        print(234234234234, data)
        if response.status_code == 201:
            return redirect('send_verification_code')
    return render(request, 'registration.html', {'form': form})


def verify_code_view(request):
    """Функция для регистрации"""
    form = InviteCodeForm(request.POST or None)

    return render(request, 'send_verification_code.html', {'form': form})


def referralview_view(request):
    """Функция для регистрации"""
    form = UserLoginForm(request.POST or None)

    return render(request, 'registration.html', {'form': form})
