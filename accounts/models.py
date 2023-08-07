from django.db import models
import string
import random


class InviteCode(models.Model):
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.code


class UserProfile(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, null=True, blank=True)
    activated_invite_code = models.ForeignKey(InviteCode, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.phone_number
