# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from skyloov.utilities.db.models import DataModel


class UserManager(BaseUserManager):
    # use_in_migrations = True
    def get_queryset(self):
        return super(UserManager, self).get_queryset()

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("users most have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin, DataModel):
    id = None
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('UUID'))
    # password = None # TODO: uncommit this while using OTP by email
    # TODO: verify email
    email = models.EmailField(max_length=128, unique=True, blank=False, null=False, verbose_name=_('Email'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is staff'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = "users"
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return '{}'.format(self.email)
