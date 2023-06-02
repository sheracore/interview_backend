# -*- coding: utf-8 -*-
from django.contrib import admin

from skyloov.users.models import UserInformation
from skyloov.utilities.admin import UserDataModelAdmin


class UserInformationAdmin(UserDataModelAdmin):
    fields = [
        'first_name',
        'last_name',
        'fullname',
        'last_login',
        'gender',
        'is_debug_mode',
        'is_staff',
        'language',
        'timezone',
    ]
    list_display = [
        'fullname',
        'last_login',
        'language',
        'timezone',
        'is_debug_mode',
        'is_staff',
    ]
    list_filter = [
        'last_login',
        'is_debug_mode',
        'is_staff',
    ]
    search_fields = [
        'first_name',
        'last_name',
        'timezone',
    ]
    exclude = []
    raw_id_fields = []
    readonly_fields = [
        'fullname',
        'last_login',
    ]
    allowed_actions = []
    inlines = []
    save_as = True

    def __init__(self, *args, **kwargs):
        Klass = UserInformationAdmin
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


admin.site.register(UserInformation, UserInformationAdmin)
