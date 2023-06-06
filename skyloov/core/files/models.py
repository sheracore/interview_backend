# -*- coding: utf-8 -*-

import tempfile

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from skyloov.utilities.db.models import (
    UserDataModel,
    UserDataModelManager,
)

from .utilities import (
    blur_hash_calculate,
    detect_type,
    get_document_path,
    validate_file,
)

"""
File Type
"""


class FileStatus(models.IntegerChoices):
    WAITING = 1
    RUNNING = 2
    FINISHED = 3
    FAILED = 4
    TIMEOUT = 5


class FileType(models.IntegerChoices):
    VOICE = 1
    IMAGE = 2
    MOVIE = 3
    PDF = 4
    PRESENTATION = 5
    SPREADSHEET = 6
    WORD = 7
    COMPRESS = 8
    TEXT = 9
    CSS = 10
    SVG = 11
    JSON = 12
    IPA = 13
    APK = 14


"""
File Model
"""


class FileModelManager(UserDataModelManager):
    pass


class FileModel(UserDataModel):
    title = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name=_('Title'),
    )
    file = models.FileField(
        upload_to=get_document_path,
        validators=[
            validate_file,
        ],
        verbose_name=_('File'),
    )
    size = models.IntegerField(
        default=0,
        verbose_name=_('File Size'),
    )
    type = models.IntegerField(
        choices=FileType.choices,
        verbose_name=_('Type'),
    )
    blur_hash = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name=_('Blur hash'),
    )
    duration = models.PositiveIntegerField(default=0, verbose_name=_('Duration'))
    key = models.CharField(max_length=16, null=True, blank=True, verbose_name=_('Key'))
    status = models.IntegerField(default=FileStatus.WAITING, choices=FileStatus.choices, verbose_name=_('Status'))

    objects = FileModelManager()

    class Meta:
        app_label = 'files'
        verbose_name = _('File model')
        verbose_name_plural = _('Files')

    def __str__(self):
        return "%s - %s" % (self.pk, self.title)

    def save(self, *args, **kwargs):
        if not self.pk:
            type_of_file = detect_type(self.file)[0]
            if type_of_file:
                self.type = type_of_file
            self.blur_hash_calculate()
        return super(FileModel, self).save(*args, **kwargs)

    def blur_hash_calculate(self):
        if self.type != FileType.IMAGE:
            self.blur_hash = None
            return

        tmp = tempfile.NamedTemporaryFile()

        # Open the file for writing.
        self.file.seek(0)
        file_binary_content = self.file.read()
        with open(tmp.name, 'wb') as f:
            f.write(file_binary_content)
        self.blur_hash = blur_hash_calculate(tmp.name)

    @property
    def path(self):
        return self.file.path


def post_save_file_model_receiver(sender, instance, created, *args, **kwargs):
    from .tasks import file_model_process

    file_model_process.delay(instance.pk)


post_save.connect(post_save_file_model_receiver, sender=FileModel)
