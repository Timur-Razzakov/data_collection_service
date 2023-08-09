import os

import requests
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from frontend.forms import UserForm
from frontend.forms import UserLoginForm, InviteCodeForm

api_url = os.environ.get('API_URL')


def logout_view(request):
    """Функция выхода"""
    logout(request)
    return redirect('frontend:home')


def home_view(request):
    form = UserForm(request.POST or None)
    # Получение CSRF-токена из кук
    csrf_token = request.COOKIES['csrftoken']
    # Определение заголовков запроса с CSRF-токеном
    headers = {
        'X-CSRFToken': csrf_token,
    }
    if form.is_valid():
        data = form.cleaned_data
        response = requests.post(
            url=f"{api_url}referral/",
            data=data, cookies=request.COOKIES, headers=headers)
        json_response = response.json()
        detail = json_response.get('detail', '')
        messages.success(request, detail)

    return render(request, 'home.html', {'form': form})


# cookies=request.COOKIES
def registration_view(request):
    """Функция для регистрации"""
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        request.session['phone_number'] = data['phone_number']
        response = requests.post(
            url=f"{api_url}registration/",
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
            url=f"{api_url}verify_code/",
            data=data)
        if response.status_code == 200:
            redirect_url = reverse('frontend:home')
            res = HttpResponseRedirect(redirect_url)
            # получаем cookie и устанавливаем в браузер
            res.set_cookie('sessionid', response.cookies.get('sessionid'))
            return res
    return render(request, 'send_verification_code.html', {
        'form': form, 'code': code})
