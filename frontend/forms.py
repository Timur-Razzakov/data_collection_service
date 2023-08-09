from accounts.models import User
from django import forms


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        label='Введите номер телефона ',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )


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


class UserForm(forms.Form):
    invite_code = forms.CharField(
        max_length=6,
        min_length=6,
        label='Введите invite_code, который хотите активировать',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
