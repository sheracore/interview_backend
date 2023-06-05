from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Q

from django.core.exceptions import ValidationError

from skyloov.shops.fields import PriceField
from skyloov.shops.products.models import Product
from skyloov.utilities.db.models import (
    UserDataModel,
    UserDataModelManager,
    UserDataModelQuerySet
)


class CartItemQuerySet  (UserDataModelQuerySet):
    pass


class CartItemManager(UserDataModelManager):
    def get_queryset(self):
        return CartItemQuerySet(self.model, using=self._db)


class CartItem(UserDataModel):
    cart = models.ForeignKey(
        'shops.cart',
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name=_('Cart'),
    )
    price = PriceField(default=0, big=True, verbose_name=_('Price'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to=Q(app_label='shops', model='product'),
    )
    object_id = models.PositiveIntegerField(verbose_name=_('Object id'))
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = CartItemManager()

    class Meta:
        unique_together = ['cart', 'object_id', 'content_type']
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')

    def __str__(self):
        return '{}'.format(self.id)

    def clean(self):
        super(CartItem, self).clean()
        if not self.content_object:
            raise ValidationError({'object_id': [_('Not found.')]})

    def save(self, *args, **kwargs):
        product = self.content_object
        self.price = product.price * self.quantity
        super(CartItem, self).save()
