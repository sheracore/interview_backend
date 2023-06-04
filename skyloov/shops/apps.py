from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShopsConfig(AppConfig):
    name = 'skyloov.shops'
    app_label = 'shops'
    verbose_name = _('Shop')
    verbose_name_plural = _('Shops')
