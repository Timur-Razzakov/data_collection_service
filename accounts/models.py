from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from django.db.models.signals import post_save

from .utils import random_string_generator

User = get_user_model()


class Referral(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    referral = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral')

    def __str__(self):
        return self.user.phone_number

    class Meta:
        unique_together = ['user', 'referral']
