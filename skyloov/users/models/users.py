# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models, transaction
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from skyloov.utilities.db.models import DataModel


class UserManager(BaseUserManager):
    # use_in_migrations = True
    def get_queryset(self):
        return super(UserManager, self).get_queryset()

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError("users most have an email address")
        try:
            with transaction.atomic():
                user = self.model(email=self.normalize_email(email), **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


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

    def info(self):
        obj = self.userinformation_set.get_or_create(
            user=self,
            is_staff=self.is_staff,
            is_active=self.is_active
        )
        return obj


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        instance.info()


post_save.connect(post_save_user_model_receiver, sender=User)
