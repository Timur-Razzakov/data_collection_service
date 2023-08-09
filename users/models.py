import string

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save

from accounts.utils import random_string_generator


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, ref_code=None, invite_code=None, activate_code=None, password=None):
        """
        Создаёт пользователя с указанным phone_number-ром
        """
        if not phone_number:
            raise ValueError('Введите номер телефона')

        user = self.model(
            phone_number=phone_number,
            invite_code=self.make_random_password(6, string.ascii_lowercase + string.digits),
            ref_code=ref_code,
            activate_code=activate_code
        )
        user.set_password(password)  # зашифровывает пароль

        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        """
        Создаёт супер пользователя для доступа к админке
        """
        user = self.create_user(
            phone_number=phone_number,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    # Валидатор, для проверки номера телефона
    phone_number_validator = RegexValidator(regex=r'^7\d{10}$',
                                            message="""Формат номера: 
                                          7XXXXXXXXXX (X - от 0 to 9)""")
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        null=False,
        blank=False,
        validators=[phone_number_validator])
    invite_code = models.CharField(max_length=6, blank=False)
    activate_code = models.CharField(max_length=4, null=True, blank=True)
    ref_code = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    list_display = ('phone_number', 'invite_code', 'ref_code', 'created_at', 'is_admin', 'is_active')

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    @staticmethod
    def has_perm(perm, obj=None):
        """Проверяет есть ли у пользователя указанное разрешение """
        return True

    @staticmethod
    def has_module_perms(app_label):
        """Есть ли у пользователя разрешение на доступ к моделям в данном приложении. """
        return True

    @property
    def is_staff(self):
        """ Является ли пользователь администратором """
        return self.is_admin


# """Сохраняем в модель UserProfile сгенерированный код"""
#
#
# # генерация происходит в utils.py
# def pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.invite_code:
#         instance.invite_code = random_string_generator(size=6)
#
#
# post_save.connect(pre_save_receiver, sender=MyUser)