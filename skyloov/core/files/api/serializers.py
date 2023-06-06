import glob
import os
import re

import requests
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from skyloov.core.files.models import FileModel
from skyloov.utilities.api.serializers import (
    UserDataModelDetailSerializer,
    UserDataModelSummarySerializer,
)
from ..enums import UploadSizeType


class FileModelSummarySerializer(UserDataModelSummarySerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = FileModel
        fields = UserDataModelSummarySerializer.Meta.fields + [
            'title',
            'link',
            'type',
            'size',
            'blur_hash',
            'duration',
            'key',
            'user',
        ]

        read_only_fields = UserDataModelSummarySerializer.Meta.read_only_fields + [
            'size',
            'link',
            'type',
            'blur_hash',
            'duration',
            'key',
            'user',
        ]

    def get_link(self, obj):
        return obj.file.url


class FileModelDetailSerializer(FileModelSummarySerializer, UserDataModelDetailSerializer):
    file = serializers.FileField(required=False, write_only=True)
    file_link = serializers.URLField(required=False, write_only=True)
    _file = None

    class Meta:
        model = FileModel
        fields = (
            UserDataModelDetailSerializer.Meta.fields
            + FileModelSummarySerializer.Meta.fields
            + [
                'file',
                'file_link',
            ]
        )

        read_only_fields = (
            UserDataModelDetailSerializer.Meta.read_only_fields
            + FileModelSummarySerializer.Meta.read_only_fields
            + []
        )

    def validate_file_link(self, value):
        if not value:
            return
        max_allow_upload_size = UploadSizeType.MEDIUM.get_size
        r = requests.head(value, allow_redirects=True)
        headers = r.headers
        mime_type = headers.get('content-type')
        file_size = headers.get('content-length', str(max_allow_upload_size))

        try:
            file_size = int(file_size)
        except ValueError:
            file_size = max_allow_upload_size

        file_name = None
        if "Content-Disposition" in r.headers.keys():
            file_name_list = re.findall("filename=(.+)", r.headers["Content-Disposition"])
            if len(file_name_list) > 0:
                file_name = file_name_list[0]

        if not file_name:
            file_name = value.split("/")[-1]

        # Check mime type
        size_error = _('Size %(size)s doesnt support.') % {
            'size': file_size,
        }
        if file_size > max_allow_upload_size:
            raise ValidationError([size_error])

        tf = TemporaryUploadedFile(file_name, mime_type, file_size, 'utf-8')
        r = requests.get(value, stream=True)
        chunk_size = 4096
        calculate_size = 0
        for chunk in r.iter_content(chunk_size=chunk_size):
            tf.write(chunk)
            calculate_size = calculate_size + chunk_size
            if calculate_size > max_allow_upload_size:
                raise ValidationError([size_error])
        tf.seek(0)
        self._file = tf

    def update(self, instance, validated_data):
        try:
            validated_data.pop('file_link')
        except Exception:
            pass
        if self._file:
            validated_data['file'] = self._file
        return super(FileModelDetailSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        try:
            validated_data.pop('file_link')
        except Exception:
            pass
        if self._file:
            validated_data['file'] = self._file
        return super(FileModelDetailSerializer, self).create(validated_data)
