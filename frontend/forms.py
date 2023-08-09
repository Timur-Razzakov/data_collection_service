from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from accounts.models import User


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'phone_number': 'Введите номер телефона:',
        }


class InviteCodeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['activate_code']
        widgets = {
            'activate_code': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'phone_number': 'Введите код активации:',
        }

#
# # Номер телефона
# # Введите код активации'
