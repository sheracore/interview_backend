import pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from faker import Faker

from skyloov.utilities.db.models import (
    UserDataModelManager,
    UserDataModelQuerySet,
    UserDataModel,
)


def default_username():
    username = Faker().user_name()[:9]
    if UserInformation.objects.filter(username=username).exists():
        pk = UserInformation.objects.all().order_by('id').last().pk
        username = f'{username}{pk}'
    return username


class LanguageType(models.TextChoices):
    ENGLISH_US = 'en_US', 'English (US)'
    ENGLISH_UK = 'en_GB', 'English (UK)'
    PERSIAN = 'fa', 'فارسی'
    ARABIC = 'ar', 'العربیه'


class GenderType(models.IntegerChoices):
    MALE = 0
    FEMALE = 1
    CUSTOM = 2


class UserInformationQuerySet(UserDataModelQuerySet):
    def staff(self):
        return self.filter(is_staff=True)


class UserInformationManager(UserDataModelManager):
    def get_queryset(self):
        return UserInformationQuerySet(self.model, using=self._db)

    def staff(self):
        return self.active().staff()


class UserInformation(UserDataModel):
    first_name = models.CharField(max_length=18, blank=True, default='', verbose_name=_('First name'))
    last_name = models.CharField(max_length=18, blank=True, default='', verbose_name=_('Last name'))
    last_login = models.DateTimeField(null=True, blank=True, verbose_name=_('Last login'))
    # TODO: is_debug_mode will be used for login without a password
    is_debug_mode = models.BooleanField(default=False, verbose_name=_('Debug mode'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is staff'))
    username = models.CharField(
        default=default_username,
        max_length=18,
        validators=[
            RegexValidator(regex=r'^\w*-*\w*$', message=_('Username must be Alphanumeric'), code='invalid_username'),
        ],
        verbose_name=_('Username'),
    )
    gender = models.IntegerField(
        null=True,
        blank=True,
        choices=GenderType.choices,
        verbose_name=_('Gender'),
    )
    timezone = models.CharField(
        max_length=100,
        choices=tuple(zip(pytz.common_timezones, pytz.common_timezones)),
        default=pytz.common_timezones[-1],
        verbose_name=_('Time zone'),
    )
    language = models.CharField(
        max_length=5, choices=LanguageType.choices, default='en_US', verbose_name=_('Language')
    )

    objects = UserInformationManager()

    class Meta:
        verbose_name = _('User information')
        verbose_name_plural = _('Users information')

    def __str__(self):
        return self.fullname

    @property
    def fullname(self):
        return '{} {}'.format(self.first_name, self.last_name)
