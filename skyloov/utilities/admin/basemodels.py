from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    fields = []
    list_filter = []
    list_display = []
    search_fields = []
    exclude = []
    raw_id_fields = []
    readonly_fields = []
    allowed_actions = []
    inlines = []


class DataModelAdmin(BaseAdmin):
    fields = [
        'pk',
        'is_active',
        'created_at',
        'update_at',
    ]
    list_display = [
        'pk',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'created_at',
    ]
    search_fields = [
        'pk',
    ]
    exclude = []
    raw_id_fields = []
    readonly_fields = [
        'pk',
        'created_at',
        'update_at',
    ]
    allowed_actions = []
    inlines = []
    save_as = True

    def __init__(self, *args, **kwargs):
        Klass = DataModelAdmin
        Klass_parent = BaseAdmin

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


class UserDataModelAdmin(DataModelAdmin):
    fields = [
        'user',
    ]
    list_display = [
        'user',
    ]
    list_filter = []
    search_fields = ['user__email', 'user__pk']
    exclude = []
    raw_id_fields = [
        'user',
    ]
    readonly_fields = []
    allowed_actions = []
    inlines = []
    save_as = True

    def __init__(self, *args, **kwargs):
        Klass = UserDataModelAdmin
        Klass_parent = DataModelAdmin

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

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if hasattr(instance, 'user_id') and not getattr(instance, 'user_id', None):
                instance.user = form.instance.user
        super(UserDataModelAdmin, self).save_formset(request, form, formset, change)
