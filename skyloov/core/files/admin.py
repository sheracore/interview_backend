# -*- coding: utf-8 -*-
from django.contrib import admin

from skyloov.core.files.models import FileModel
from skyloov.utilities.admin import UserDataModelAdmin


class FileModelAdmin(UserDataModelAdmin):
    fields = [
        'title',
        'file',
        'size',
        'type',
        'blur_hash',
        'duration',
        'status',
    ]
    list_display = [
        'title',
        'size',
        'type',
        'duration',
        'status',
    ]
    list_filter = [
        'type',
        'status',
    ]
    search_fields = [
        'title',
    ]
    exclude = []
    raw_id_fields = []
    readonly_fields = [
        'size',
        'blur_hash',
        'duration',
    ]
    allowed_actions = []
    inlines = []

    def __init__(self, *args, **kwargs):
        Klass = FileModelAdmin
        Klass_parent = UserDataModelAdmin

        super(Klass, self).__init__(*args, **kwargs)

        self.fields = Klass_parent.fields + self.fields
        self.list_display = Klass_parent.list_display + self.list_display
        self.list_filter = Klass_parent.list_filter + self.list_filter
        self.search_fields = Klass_parent.search_fields + self.search_fields
        self.exclude = Klass_parent.exclude + self.exclude
        self.raw_id_fields = Klass_parent.raw_id_fields + self.raw_id_fields
        self.readonly_fields = Klass_parent.readonly_fields + self.readonly_fields
        self.allowed_actions = Klass_parent.allowed_actions + self.allowed_actions
        self.inlines = Klass_parent.inlines + self.inlines


admin.site.register(FileModel, FileModelAdmin)
