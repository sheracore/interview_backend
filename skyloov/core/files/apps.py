# -*- coding: utf-8 -*-


from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FileConfig(AppConfig):
    name = 'skyloov.core.files'
    app_label = 'files'
    label = 'files'
    verbose_name = _('Files')
