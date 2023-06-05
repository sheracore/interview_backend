from django.db import models
from django.utils.translation import gettext_lazy as _
from skyloov.utilities.db.models import (
    UserDataModel,
    UserDataModelManager,
    UserDataModelQuerySet
)


class CartQuerySet(UserDataModelQuerySet):
    pass


class CartManager(UserDataModelManager):
    def get_queryset(self):
        return CartQuerySet(self.model, using=self._db)


class Cart(UserDataModel):
    title = models.CharField(blank=True, max_length=25, verbose_name=_('Title'))

    objects = CartManager()

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return '{}'.format(self.id)

    @property
    def total_price(self):
        item_price = [item.price for item in self.items.all()]
        price = sum(item_price)
        return price
