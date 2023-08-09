from django.contrib import admin
from .models import MyUser
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group


# class UserCreationForm(forms.ModelForm):
#     """Форма для заполнения пароля и создание пользователя"""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#     phone_number = forms.CharField(label='phone_number', widget=forms.TextInput)
#
#     class Meta:
#         model = MyUser
#         fields = ('phone_number', 'activate_code')
#
#     def clean_password2(self):
#         """Проверяет пароли на совпадение между собой"""
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Пароль не совпадает")
#         return password2
#
#     def save(self, commit=True):
#         """ Производим сохранение пользователя """
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()
#     invite_code = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = MyUser
#         fields = (
#             'phone_number', 'invite_code', 'activate_code', 'ref_code',
#             'is_active', 'is_admin')
#
#     def clean_password(self):
#         # Независимо от того, что предоставил пользователь, вернуть начальное значение.
#         # Это делается здесь, а не на поле, потому что
#         # поле не имеет доступа к начальному значению
#         return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # Формы для добавления и изменения пользовательских экземпляров
    # form = UserChangeForm
    # add_form = UserCreationForm

    list_display = ('phone_number', 'invite_code', 'activate_code', 'ref_code',
                    'is_active', 'is_admin')
    list_filter = ('is_admin',)
    # Определение списка полей, доступных только для чтения
    readonly_fields = ('invite_code', 'activate_code')
    fieldsets = (
        # Поля для Отображения в админке
        (None, {'fields': ('phone_number', 'invite_code', 'activate_code', 'ref_code',)}),

        ('Permissions', {'fields': ('is_admin','is_active')}),
    )

    """ Поля которые будут использоваться при создании пользователя """
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'activate_code', ),
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
""" отмена регистрацию модели группы от администратора"""
admin.site.unregister(Group)
