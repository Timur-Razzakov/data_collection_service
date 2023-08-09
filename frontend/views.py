import os
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from frontend.forms import UserLoginForm, InviteCodeForm

from accounts.models import User

# api_url = os.environ.get('API_URL')
# print(api_url)
API_URL = "http://127.0.0.1:8800/api/"


def logout_view(request):
    """Функция выхода"""
    logout(request)
    return redirect('home')


def home_view(request):
    """Домашняя страница"""
    return render(request, 'home.html', )


# cookies=request.COOKIES
def registration_view(request):
    """Функция для регистрации"""

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data

        request.session['phone_number'] = data['phone_number']
        response = requests.post(
            url=f"{API_URL}registration/",
            data=data, )
        if response.status_code == 200:
            json_response = response.json()
            code_value = json_response.get('auth_code', '')
            return redirect('frontend:verify_code', code=code_value)
    return render(request, 'registration.html', {'form': form})


def verify_code_view(request, code):
    """Функция для авторизации по коду"""
    form = InviteCodeForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        data['phone_number'] = request.session.get('phone_number', None)
        response = requests.post(
            url=f"{API_URL}verify_code/",
            data=data)
        if response.status_code == 200:
            current_user = User.objects.filter(phone_number=data['phone_number']).first()
            # user = authenticate(request, phone_number=data['phone_number'])
            if current_user:
                login(request, current_user)
                #
                return redirect('frontend:home')
            else:
                error_message = 'Неверный номер телефона или код'
                print(error_message)
    return render(request, 'send_verification_code.html', {'form': form, 'code': code})


def referral_view(request):
    """рефералы"""
    form = UserLoginForm(request.POST or None)

    return render(request, 'registration.html', {'form': form})
