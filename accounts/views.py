import datetime as dt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from accounts.forms import UserLoginForm, UserRegistrationForm, ContactForm, UserUpdateForm
from icecream import ic
from scraping.models import Error

User = get_user_model()

"""Функция для авторизации"""


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


"""Функция выхода"""


def logout_view(request):
    logout(request)
    return redirect('home')


""" Функция для создание нового пользователя """


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)  # instans) commit=False-->исп для полного соединения с базой
        new_user.set_password(form.cleaned_data['password'])  # ЗАШИФРОВЫВАЕТ пароль
        new_user.save()
        messages.success(request, 'Пользователь добавлен в систему.')
        return render(request, 'accounts/registered.html',
                      {'new_user': new_user})
    return render(request, 'accounts/registration.html', {'form': form})


"""
Функция для обновлений данных указанных ранее 
"""


def update_view(request):
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.speciality = data['speciality']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данные сохранены.')
                return redirect('update')
        form = UserUpdateForm(
            initial={'city': user.city, 'speciality': user.speciality,
                     'send_email': user.send_email})
        return render(request, 'accounts/update.html',
                      {'form': form, 'contact_form': contact_form})
    else:
        return redirect('login')


"""Функция для удаления пользователя"""


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удалён :(')
    return redirect('home')


def contact_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            ic(type(data))
            city = data.get('city')
            speciality = data.get('speciality')
            email = data.get('email')
            qs = Error.objects.filter(created_at=dt.date.today())
            if qs.exists():
                err = qs.first()
                ic(err)
                ic(type(err))
                data = err.data.get('user_data', [])
                ic(type(data))
                data.append({'city': city, 'email': email, 'speciality': speciality})
                err.data['user_data'] = data
                err.save()
            else:
                data = [{'city': city, 'email': email, 'speciality': speciality}]
                Error(data=f"user_data:{data}").save()
            messages.success(request, 'Данные отправлены администрации.')
            return redirect('update')
        else:
            return redirect('update')
    else:
        return redirect('login')
