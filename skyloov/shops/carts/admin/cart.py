from django.contrib import admin
from skyloov.utilities.admin import UserDataModelAdmin
from ..models import Cart, CartItem


class OrderItemInline(admin.TabularInline):
    model = CartItem
    ct_field = "content_type"
    ct_fk_field = "object_id"
    extra = 1
    fields = [
        'user',
        'price',
        'quantity',
        'content_type',
        'object_id'
    ]
    readonly_fields = [
        'user',
        'price',
    ]


class CartAdmin(UserDataModelAdmin):
    fields = [
        'title',
        'total_price'
    ]
    list_display = [
        'title',
        'total_price'
    ]
    list_filter = [
    ]
    search_fields = [
        'title',
    ]
    exclude = []
    raw_id_fields = []
    readonly_fields = [
        'total_price'
    ]
    allowed_actions = []
    inlines = [
        OrderItemInline
    ]

    def __init__(self, *args, **kwargs):
        Klass = CartAdmin
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


admin.site.register(Cart, CartAdmin)
